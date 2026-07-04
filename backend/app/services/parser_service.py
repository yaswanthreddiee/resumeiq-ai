from pathlib import Path

import fitz
from docx import Document

from app.utils.exceptions import BadRequestException


class ParserService:
    """
    Extract plain text from resumes.
    """

    async def extract_text(
        self,
        file_path: str,
        extension: str,
    ) -> str:

        extension = extension.lower()

        if extension == "pdf":
            return self._extract_pdf(file_path)

        if extension == "docx":
            return self._extract_docx(file_path)

        raise BadRequestException(
            "Unsupported file."
        )

    def _extract_pdf(self, path: str) -> str:

        document = fitz.open(path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    def _extract_docx(self, path: str) -> str:

        document = Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )