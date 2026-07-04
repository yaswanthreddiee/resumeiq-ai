from app.ai.base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):

    async def analyze_ats(self, resume_content: dict):
        raise NotImplementedError("OpenAI provider coming soon.")

    async def match_job_description(
        self,
        resume_content: dict,
        job_description: str,
    ):
        raise NotImplementedError("OpenAI provider coming soon.")