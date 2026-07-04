import json

import google.generativeai as genai

from app.ai.base import BaseAIProvider
from app.config import settings
from app.utils.logger import logger


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini AI Provider.
    """

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            settings.AI_MODEL
        )

    async def analyze_ats(
        self,
        resume_content: dict,
    ) -> dict:

        prompt = f"""
You are an ATS Resume Expert.

Analyze this resume.

Return ONLY valid JSON.

Resume:

{resume_content["raw_text"]}

Return JSON in this format:

{{
    "overall_score":80,
    "keyword_match":75,
    "grammar_score":90,
    "formatting_score":88,
    "action_verb_score":82,
    "missing_skills":[
        "Docker",
        "AWS"
    ],
    "suggestions":[
        "Improve projects",
        "Add measurable achievements"
    ]
}}
"""

        try:

            response = self.model.generate_content(prompt)

            text = response.text.strip()

            print("\n========== GEMINI RESPONSE ==========")
            print(text)
            print("=====================================\n")

            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()

            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:
                text = text[start:end + 1]

            return json.loads(text)

        except Exception as e:
            logger.error(f"Gemini ATS Error: {e}")
            raise

    async def match_job_description(
        self,
        resume_content: dict,
        job_description: str,
    ) -> dict:

        prompt = f"""
Compare the resume with the job description.

Return ONLY valid JSON.

Resume:

{resume_content["raw_text"]}

Job Description:

{job_description}

Return JSON like:

{{
    "match_percentage":82,
    "matched_keywords":[
        "Python",
        "FastAPI"
    ],
    "missing_keywords":[
        "Docker",
        "AWS"
    ],
    "suggestions":[
        "Mention Docker",
        "Mention AWS"
    ]
}}
"""

        try:

            response = self.model.generate_content(prompt)

            text = response.text.strip()

            print("\n========== GEMINI MATCH RESPONSE ==========")
            print(text)
            print("===========================================\n")

            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()

            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:
                text = text[start:end + 1]

            return json.loads(text)

        except Exception as e:
            logger.error(f"Gemini Match Error: {e}")
            raise