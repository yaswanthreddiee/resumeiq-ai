from fastapi import UploadFile

from app.ai.resume_parser import ResumeParser
from app.repositories.resume_repository import ResumeRepository
from app.services.ai_service import AIService
from app.services.file_service import FileService
from app.services.parser_service import ParserService
from app.utils.exceptions import NotFoundException
from app.utils.logger import logger


class ResumeService:
    """
    Business logic for resume operations.
    """

    def __init__(self, db):

        self.file_service = FileService()
        self.parser_service = ParserService()
        self.resume_parser = ResumeParser()
        self.ai_service = AIService()
        self.repository = ResumeRepository(db)

    # --------------------------------------------------
    # Upload Resume
    # --------------------------------------------------

    async def upload_resume(
        self,
        user_id: str,
        file: UploadFile,
    ):

        try:

            saved_file = await self.file_service.save_file(file)

            raw_text = await self.parser_service.extract_text(
                saved_file["path"],
                saved_file["extension"],
            )

            parsed_resume = await self.resume_parser.parse(
                raw_text
            )

            resume = await self.repository.create_resume(
                user_id=user_id,
                filename=saved_file["filename"],
                stored_path=saved_file["path"],
                parsed_content=parsed_resume,
            )

            return {
                "_id": str(resume["_id"]),
                "user_id": user_id,
                "file_name": resume["file_name"],
                "file_url": resume["file_url"],
                "parsed_content": resume["parsed_content"],
                "uploaded_at": resume["uploaded_at"],
            }

        except Exception as e:
            logger.error(f"Upload Resume Error: {e}")
            raise

    # --------------------------------------------------
    # Resume CRUD
    # --------------------------------------------------

    async def get_resume(
        self,
        resume_id: str,
        user_id: str,
    ):

        resume = await self.repository.get_resume(
            resume_id,
            user_id,
        )

        if resume is None:
            raise NotFoundException("Resume not found")

        return resume

    async def get_resumes(
        self,
        user_id: str,
    ):

        return await self.repository.list_resumes(
            user_id,
        )

    async def delete_resume(
        self,
        resume_id: str,
        user_id: str,
    ):

        resume = await self.repository.delete_resume(
            resume_id,
            user_id,
        )

        if resume is None:
            raise NotFoundException("Resume not found")

        self.file_service.delete_file(
            resume["file_url"],
        )

        await self.repository.delete_resume_related_data(
            resume_id,
        )

        return {
            "message": "Resume deleted successfully"
        }

    # --------------------------------------------------
    # ATS Analysis
    # --------------------------------------------------

    async def analyze_ats(
        self,
        resume_id: str,
        user_id: str,
    ):

        resume = await self.get_resume(
            resume_id,
            user_id,
        )

        analysis = await self.ai_service.analyze_ats(
            resume["parsed_content"]
        )

        await self.repository.update_ats_score(
            resume_id,
            analysis,
        )

        await self.repository.save_ats_analysis(
            resume_id,
            user_id,
            analysis,
        )

        return analysis

    async def get_ats_score(
        self,
        resume_id: str,
        user_id: str,
    ):

        analysis = await self.repository.get_ats_analysis(
            resume_id,
            user_id,
        )

        if analysis is None:
            raise NotFoundException(
                "ATS analysis not found"
            )

        return analysis

    # --------------------------------------------------
    # Job Matching
    # --------------------------------------------------

    async def match_job_description(
        self,
        resume_id: str,
        user_id: str,
        job_description: str,
    ):

        resume = await self.get_resume(
            resume_id,
            user_id,
        )

        result = await self.ai_service.match_job_description(
            resume["parsed_content"],
            job_description,
        )

        await self.repository.save_job_match(
            resume_id,
            user_id,
            job_description,
            result,
        )

        return result

    async def get_job_matching(
        self,
        resume_id: str,
        user_id: str,
    ):

        result = await self.repository.get_job_match(
            resume_id,
            user_id,
        )

        if result is None:
            raise NotFoundException(
                "Job matching not found"
            )

        return result