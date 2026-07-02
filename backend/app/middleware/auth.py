"""Authentication middleware."""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.security import decode_token
from app.utils.logger import logger


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for JWT authentication."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and validate JWT token."""
        # Skip auth for public endpoints
        public_paths = ["/", "/health", "/docs", "/redoc", "/openapi.json"]
        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)
        
        # Skip auth for auth endpoints
        if request.url.path.startswith("/api/auth/"):
            if request.method == "POST" and request.url.path in ["/api/auth/signup", "/api/auth/login"]:
                return await call_next(request)
        
        # Get token from header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authentication token")
        
        token = auth_header.split(" ")[1]
        
        try:
            payload = decode_token(token)
            request.state.user_id = payload.get("sub")
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return await call_next(request)
