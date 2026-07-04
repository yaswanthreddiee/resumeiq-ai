"""Authentication middleware."""

from bson import ObjectId
from fastapi import Depends, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.database.mongo import get_db
from app.utils.logger import logger
from app.utils.security import decode_token


class AuthMiddleware(BaseHTTPMiddleware):
    """JWT Authentication Middleware."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # -------------------------
        # Public endpoints
        # -------------------------
        if (
            path == "/"
            or path == "/health"
            or path.startswith("/docs")
            or path.startswith("/redoc")
            or path.startswith("/openapi")
        ):
            return await call_next(request)

        # -------------------------
        # Public Authentication APIs
        # -------------------------
        if (
        (request.method == "POST" and path in (
            "/api/auth/signup",
            "/api/auth/login",
            "/api/auth/forgot-password",
        ))
        or path == "/api/auth/test-ai"
    ):
            return await call_next(request)
        

        # -------------------------
        # Read Authorization Header
        # -------------------------
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
        status_code=401,
        content={"detail": "Authorization header missing"},
    )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"},
            )

        token = auth_header.split(" ", 1)[1]

        try:
            payload = decode_token(token)

            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token payload",
                )

            request.state.user_id = user_id

        except HTTPException as e:
            return JSONResponse(
        status_code=e.status_code,
        content={"detail": e.detail},
    )

        except Exception as e:
            logger.error(f"JWT Error: {e}")

            return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or expired token"},
    )

        return await call_next(request)


async def get_current_user(
    request: Request,
    db=Depends(get_db),
):
    """
    Return authenticated user.
    """

    user_id = getattr(request.state, "user_id", None)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    try:
        user = await db.users.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid user id",
        )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


async def get_admin_user(
    current_user=Depends(get_current_user),
):
    """
    Return authenticated admin.
    """

    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user

