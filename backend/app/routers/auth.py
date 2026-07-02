"""Authentication router."""

from fastapi import APIRouter, Depends, HTTPException, Request
from bson import ObjectId
from app.schemas.schemas import UserSignupSchema, UserLoginSchema, TokenResponseSchema, UpdateProfileSchema
from app.controllers.auth_controller import AuthController
from app.database.mongo import get_db
from app.utils.exceptions import AppException
from app.utils.logger import logger

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
async def get_current_user(
    request: Request,
    db = Depends(get_db)
):
    """Get current authenticated user."""
    try:
        user_id = request.state.user_id
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "_id": str(user["_id"]),
            "email": user["email"],
            "name": user["name"],
            "role": user.get("role", "user"),
            "created_at": user["created_at"],
            "updated_at": user["updated_at"],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
    request: Request,
    controller: AuthController = Depends(get_auth_controller)
):
    """Update user profile."""
    try:
        user_id = request.state.user_id
        return await controller.update_profile(user_id, data.dict(exclude_unset=True))
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
