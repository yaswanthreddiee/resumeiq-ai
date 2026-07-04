from app.ai.base import BaseAIProvider


class OllamaProvider(BaseAIProvider):

    async def analyze_ats(self, resume_content: dict):
        raise NotImplementedError("Ollama provider coming soon.")

    async def match_job_description(
        self,
        resume_content: dict,
        job_description: str,
    ):
        raise NotImplementedError("Ollama provider coming soon.")