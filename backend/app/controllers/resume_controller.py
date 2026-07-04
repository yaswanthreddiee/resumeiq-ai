from fastapi import UploadFile

from app.services.resume_service import ResumeService


class ResumeController:
    """
    Controller responsible for coordinating resume requests.
    """

    def __init__(self, db):
        self.resume_service = ResumeService(db)

    # --------------------------------------------------
    # Resume CRUD
    # --------------------------------------------------

    async def upload_resume(
        self,
        user_id: str,
        file: UploadFile,
    ):
        return await self.resume_service.upload_resume(
            user_id,
            file,
        )

    async def get_resumes(
        self,
        user_id: str,
    ):
        return await self.resume_service.get_resumes(
            user_id,
        )

    async def get_resume(
        self,
        resume_id: str,
        user_id: str,
    ):
        return await self.resume_service.get_resume(
            resume_id,
            user_id,
        )

    async def delete_resume(
        self,
        resume_id: str,
        user_id: str,
    ):
        return await self.resume_service.delete_resume(
            resume_id,
            user_id,
        )

    # --------------------------------------------------
    # ATS Analysis
    # --------------------------------------------------

    async def analyze_ats(
        self,
        resume_id: str,
        user_id: str,
    ):
        return await self.resume_service.analyze_ats(
            resume_id,
            user_id,
        )

    async def get_ats_score(
        self,
        resume_id: str,
        user_id: str,
    ):
        return await self.resume_service.get_ats_score(
            resume_id,
            user_id,
        )

    # --------------------------------------------------
    # Job Matching
    # --------------------------------------------------

    async def match_job_description(
        self,
        resume_id: str,
        user_id: str,
        job_description: str,
    ):
        return await self.resume_service.match_job_description(
            resume_id,
            user_id,
            job_description,
        )

    async def get_job_matching(
        self,
        resume_id: str,
        user_id: str,
    ):
        return await self.resume_service.get_job_matching(
            resume_id,
            user_id,
        )