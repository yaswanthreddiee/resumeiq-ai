"""Authentication router."""
from app.services.ai_service import AIService
from fastapi import APIRouter, Depends, HTTPException, Request
from bson import ObjectId
from app.schemas.schemas import UserSignupSchema, UserLoginSchema, TokenResponseSchema, UpdateProfileSchema
from app.controllers.auth_controller import AuthController
from app.database.mongo import get_db
from app.utils.exceptions import AppException
from app.utils.logger import logger
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_controller(db = Depends(get_db)):
    """Get auth controller instance."""
    return AuthController(db)


@router.post("/signup", response_model=TokenResponseSchema, status_code=201)
async def signup(
    data: UserSignupSchema,
    controller: AuthController = Depends(get_auth_controller)
):
    """Register new user."""
    try:
        return await controller.signup(data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login", response_model=TokenResponseSchema)
async def login(
    data: UserLoginSchema,
    controller: AuthController = Depends(get_auth_controller)
):
    """Authenticate user."""
    try:
        return await controller.login(data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/me")
async def get_me(
    request: Request,
    db=Depends(get_db),
):
    """Get current authenticated user."""

    user_id = getattr(request.state, "user_id", None)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    user = await db.users.find_one(
        {"_id": ObjectId(user_id)}
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "role": user.get("role", "user"),
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    controller: AuthController = Depends(get_auth_controller)
):
    """Request password reset."""
    try:
        return await controller.forgot_password(email)
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/profile")
async def update_profile(
    data: UpdateProfileSchema,
    current_user=Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller),
):
    try:
        return await controller.update_profile(
            str(current_user["_id"]),
            data.model_dump(exclude_unset=True),
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

from app.services.ai_service import AIService

@router.get("/test-ai")
async def test_ai():
    ai = AIService()

    response = await ai.client.chat.completions.create(
        model="gpt-4o-mini",   # use this temporarily
        messages=[
            {
                "role": "user",
                "content": "Say hello."
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }