"""
AI Service

Chooses which AI provider to use.
"""

from app.config import settings

from app.ai.gemini_provider import GeminiProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.groq_provider import GroqProvider
from app.ai.ollama_provider import OllamaProvider


class AIService:

    def __init__(self):

        provider = settings.AI_PROVIDER.lower()

        if provider == "gemini":
            self.provider = GeminiProvider()

        elif provider == "openai":
            self.provider = OpenAIProvider()

        elif provider == "groq":
            self.provider = GroqProvider()

        elif provider == "ollama":
            self.provider = OllamaProvider()

        else:
            raise ValueError(
                f"Unsupported AI Provider: {provider}"
            )

    async def analyze_ats(
        self,
        resume_content: dict,
    ):
        return await self.provider.analyze_ats(
            resume_content
        )

    async def match_job_description(
        self,
        resume_content: dict,
        job_description: str,
    ):
        return await self.provider.match_job_description(
            resume_content,
            job_description,
        )