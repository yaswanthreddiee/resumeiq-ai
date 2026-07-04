from app.ai.base import BaseAIProvider


class GroqProvider(BaseAIProvider):

    async def analyze_ats(self, resume_content: dict):
        raise NotImplementedError("Groq provider coming soon.")

    async def match_job_description(
        self,
        resume_content: dict,
        job_description: str,
    ):
        raise NotImplementedError("Groq provider coming soon.")