import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -----------------------
    # App
    # -----------------------
    APP_NAME: str = "ResumeIQ AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    # -----------------------
    # Server
    # -----------------------
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # -----------------------
    # Database
    # -----------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "resumeiq")

    # -----------------------
    # JWT
    # -----------------------
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "your-secret-key-change-in-production",
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(
        os.getenv("JWT_EXPIRATION_HOURS", "24")
    )

    # -----------------------
    # OpenAI
    # -----------------------
# -----------------------
# AI Provider
# -----------------------

    # -----------------------
    # AI Provider
    # -----------------------
    AI_PROVIDER: str = os.getenv(
        "AI_PROVIDER",
        "gemini",
    )

    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        "",
    )

    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        "",
    )

    OLLAMA_URL: str = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434",
    )

    AI_MODEL: str = os.getenv(
        "AI_MODEL",
        "gemini-2.5-flash",
    )
    # -----------------------
    # Upload
    # -----------------------
    MAX_UPLOAD_SIZE: int = int(
        os.getenv("MAX_UPLOAD_SIZE", "10485760")
    )

    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx"]

    UPLOAD_DIR: str = os.getenv(
        "UPLOAD_DIR",
        "uploads",
    )

    # -----------------------
    # CORS
    # -----------------------
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://localhost:3000,http://localhost:8000",
        ).split(",")
    )

    # -----------------------
    # Rate Limit
    # -----------------------
    RATE_LIMIT_REQUESTS: int = int(
        os.getenv("RATE_LIMIT_REQUESTS", "100")
    )

    RATE_LIMIT_WINDOW_MINUTES: int = int(
        os.getenv("RATE_LIMIT_WINDOW_MINUTES", "15")
    )

    # -----------------------
    # Email
    # -----------------------
    SMTP_SERVER: str = os.getenv(
        "SMTP_SERVER",
        "smtp.gmail.com",
    )

    SMTP_PORT: int = int(
        os.getenv("SMTP_PORT", "587")
    )

    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    # -----------------------
    # Admin
    # -----------------------
    ADMIN_EMAIL: str = os.getenv(
        "ADMIN_EMAIL",
        "admin@resumeiq.com",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()