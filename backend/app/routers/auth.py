from fastapi import APIRouter, Depends, status
from app.schemas.schemas import UserSignupSchema, UserLoginSchema, UserSchema, TokenSchema
from app.controllers.auth_controller import AuthController
from app.middleware.auth import get_current_user
from app.database.mongo import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def signup(data: UserSignupSchema, db = Depends(get_db)):
    """User signup."""
    controller = AuthController(db)
    return await controller.signup(data)

@router.post("/login", response_model=TokenSchema)
async def login(data: UserLoginSchema, db = Depends(get_db)):
    """User login."""
    controller = AuthController(db)
    return await controller.login(data)

@router.get("/me", response_model=UserSchema)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information."""
    return {
        "_id": str(current_user["_id"]),
        "email": current_user["email"],
        "name": current_user["name"],
        "role": current_user.get("role", "user"),
        "created_at": current_user["created_at"],
        "updated_at": current_user["updated_at"],
    }

@router.post("/forgot-password")
async def forgot_password(email: str, db = Depends(get_db)):
    """Request password reset."""
    controller = AuthController(db)
    return await controller.forgot_password(email)

@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db = Depends(get_db)):
    """Reset password."""
    controller = AuthController(db)
    return await controller.reset_password(token, new_password)

@router.put("/profile")
async def update_profile(data: dict, current_user = Depends(get_current_user), db = Depends(get_db)):
    """Update user profile."""
    controller = AuthController(db)
    return await controller.update_profile(str(current_user["_id"]), data)
