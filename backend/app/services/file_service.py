from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings
from app.utils.exceptions import BadRequestException


class FileService:
    """
    Handles physical file operations.

    Responsibilities:
        - Validate uploaded files
        - Save files
        - Delete files
    """

    ALLOWED_EXTENSIONS = {"pdf", "docx"}

    def __init__(self) -> None:
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile) -> dict:
        """
        Validate and save uploaded file.

        Returns
        -------
        {
            "filename": "...",
            "stored_name": "...",
            "path": "...",
            "extension": "pdf"
        }
        """

        if not file.filename:
            raise BadRequestException("Filename is missing.")

        extension = file.filename.split(".")[-1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise BadRequestException(
                f"Unsupported file type: {extension}"
            )

        stored_name = f"{uuid.uuid4()}.{extension}"

        destination = self.upload_dir / stored_name

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": file.filename,
            "stored_name": stored_name,
            "path": str(destination),
            "extension": extension,
        }

    def delete_file(self, path: str) -> None:
        """
        Delete uploaded file.
        """

        file_path = Path(path)

        if file_path.exists():
            file_path.unlink()


    