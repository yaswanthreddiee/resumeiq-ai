"""AI service for resume analysis using OpenAI."""

import openai
from typing import Dict, Any, List
from app.config import settings
from app.utils.logger import logger


class AIService:
    """Service for AI-powered resume analysis."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def analyze_ats(self, resume_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume for ATS compatibility."""
        try:
            prompt = self._build_ats_analysis_prompt(resume_content)
            response = await self._call_gpt(prompt)
            return self._parse_ats_response(response)
        except Exception as e:
            logger.error(f"Error analyzing ATS: {e}")
            raise
    
    async def match_job_description(self, resume_content: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Match resume with job description."""
        try:
            prompt = self._build_matching_prompt(resume_content, job_description)
            response = await self._call_gpt(prompt)
            return self._parse_matching_response(response)
        except Exception as e:
            logger.error(f"Error matching job description: {e}")
            raise
    
    async def _call_gpt(self, prompt: str) -> str:
        """Call GPT API."""
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert resume analyst and ATS specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"GPT API error: {e}")
            raise
    
    def _build_ats_analysis_prompt(self, resume_content: Dict[str, Any]) -> str:
        """Build prompt for ATS analysis."""
        return f"""
Analyze this resume for ATS compatibility and provide a detailed score.

Resume Content:
{resume_content.get('raw_text', '')}

Provide the response in this exact format:
OVERALL_SCORE: [0-100]
KEYWORD_MATCH: [0-100]
GRAMMAR_SCORE: [0-100]
FORMATTING_SCORE: [0-100]
ACTION_VERB_SCORE: [0-100]
MISSING_SKILLS: [comma-separated list]
SUGGESTIONS: [numbered list of suggestions]
"""
    
    def _build_matching_prompt(self, resume_content: Dict[str, Any], job_description: str) -> str:
        """Build prompt for job matching."""
        return f"""
Match this resume against the job description and provide match percentage.

Resume:
{resume_content.get('raw_text', '')}

Job Description:
{job_description}

Provide the response in this exact format:
MATCH_PERCENTAGE: [0-100]
MATCHED_KEYWORDS: [comma-separated list]
MISSING_KEYWORDS: [comma-separated list]
SUGGESTIONS: [numbered list of suggestions]
"""
    
    def _parse_ats_response(self, response: str) -> Dict[str, Any]:
        """Parse ATS analysis response."""
        lines = response.split("\n")
        result = {
            "overall_score": 75.0,
            "keyword_match": 70.0,
            "grammar_score": 80.0,
            "formatting_score": 75.0,
            "action_verb_score": 70.0,
            "missing_skills": [],
            "suggestions": [],
            "section_analysis": []
        }
        
        for line in lines:
            if "OVERALL_SCORE" in line:
                try:
                    result["overall_score"] = float(line.split(":")[1].strip())
                except:
                    pass
            elif "KEYWORD_MATCH" in line:
                try:
                    result["keyword_match"] = float(line.split(":")[1].strip())
                except:
                    pass
            elif "GRAMMAR_SCORE" in line:
                try:
                    result["grammar_score"] = float(line.split(":")[1].strip())
                except:
                    pass
            elif "FORMATTING_SCORE" in line:
                try:
                    result["formatting_score"] = float(line.split(":")[1].strip())
                except:
                    pass
            elif "ACTION_VERB_SCORE" in line:
                try:
                    result["action_verb_score"] = float(line.split(":")[1].strip())
                except:
                    pass
            elif "MISSING_SKILLS" in line:
                try:
                    skills_str = line.split(":")[1].strip()
                    result["missing_skills"] = [s.strip() for s in skills_str.split(",") if s.strip()]
                except:
                    pass
            elif "SUGGESTIONS" in line:
                try:
                    sugg_str = line.split(":")[1].strip()
                    result["suggestions"] = [s.strip() for s in sugg_str.split(",") if s.strip()]
                except:
                    pass
        
        return result
    
    def _parse_matching_response(self, response: str) -> Dict[str, Any]:
        """Parse job matching response."""
        lines = response.split("\n")
        result = {
            "match_percentage": 75.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": []
        }
        
        for line in lines:
            if "MATCH_PERCENTAGE" in line:
                try:
                    result["match_percentage"] = float(line.split(":")[1].strip())
                except:
                    pass
            elif "MATCHED_KEYWORDS" in line:
                try:
                    keywords_str = line.split(":")[1].strip()
                    result["matched_keywords"] = [k.strip() for k in keywords_str.split(",") if k.strip()]
                except:
                    pass
            elif "MISSING_KEYWORDS" in line:
                try:
                    keywords_str = line.split(":")[1].strip()
                    result["missing_keywords"] = [k.strip() for k in keywords_str.split(",") if k.strip()]
                except:
                    pass
            elif "SUGGESTIONS" in line:
                try:
                    sugg_str = line.split(":")[1].strip()
                    result["suggestions"] = [s.strip() for s in sugg_str.split(",") if s.strip()]
                except:
                    pass
        
        return result
