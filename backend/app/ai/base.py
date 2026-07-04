from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """
    Base class for all AI providers.
    """

    @abstractmethod
    async def analyze_ats(self, resume_content: dict) -> dict:
        """
        Analyze resume for ATS score.
        """
        pass

    @abstractmethod
    async def match_job_description(
        self,
        resume_content: dict,
        job_description: str,
    ) -> dict:
        """
        Match resume against job description.
        """
        pass