from datetime import datetime
from bson import ObjectId
from app.schemas.schemas import UserSignupSchema, UserLoginSchema
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.exceptions import ConflictException, NotFoundException, BadRequestException

class AuthController:
    def __init__(self, db):
        self.db = db
    
    async def signup(self, data: UserSignupSchema):
        """Register new user."""
        # Check if user exists
        existing_user = await self.db.users.find_one({"email": data.email})
        if existing_user:
            raise ConflictException("Email already registered")
        
        # Create user
        user = {
            "email": data.email,
            "name": data.name,
            "password_hash": hash_password(data.password),
            "role": "user",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        result = await self.db.users.insert_one(user)
        user["_id"] = result.inserted_id
        
        # Generate token
        access_token = create_access_token({"sub": str(result.inserted_id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "_id": str(result.inserted_id),
                "email": user["email"],
                "name": user["name"],
                "role": user["role"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
            },
        }
    
    async def login(self, data: UserLoginSchema):
        """Authenticate user."""
        user = await self.db.users.find_one({"email": data.email})
        if not user or not verify_password(data.password, user["password_hash"]):
            raise BadRequestException("Invalid email or password")
        
        # Generate token
        access_token = create_access_token({"sub": str(user["_id"])})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "_id": str(user["_id"]),
                "email": user["email"],
                "name": user["name"],
                "role": user.get("role", "user"),
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
            },
        }
    
    async def forgot_password(self, email: str):
        """Request password reset."""
        user = await self.db.users.find_one({"email": email})
        if not user:
            # Don't reveal if user exists
            return {"message": "If user exists, password reset email will be sent"}
        
        # TODO: Implement email sending
        return {"message": "Password reset email sent"}
    
    async def reset_password(self, token: str, new_password: str):
        """Reset password with token."""
        # TODO: Verify reset token
        return {"message": "Password reset successfully"}
    
    async def update_profile(self, user_id: str, data: dict):
        """Update user profile."""
        update_data = {}
        if "name" in data:
            update_data["name"] = data["name"]
        if "email" in data:
            # Check if new email is unique
            existing = await self.db.users.find_one({"email": data["email"], "_id": {"$ne": ObjectId(user_id)}})
            if existing:
                raise ConflictException("Email already in use")
            update_data["email"] = data["email"]
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.db.users.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise NotFoundException("User not found")
        
        return {
            "_id": str(result["_id"]),
            "email": result["email"],
            "name": result["name"],
            "role": result.get("role", "user"),
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }


