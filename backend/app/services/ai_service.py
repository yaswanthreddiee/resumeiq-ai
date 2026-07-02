import json
from typing import Dict, List, Any
from app.config import settings

class AIService:
    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            print(f"Warning: OpenAI client not initialized: {e}")
            self.client = None
    
    async def analyze_ats(self, resume_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume for ATS compatibility."""
        if not self.client:
            return self._mock_ats_analysis()
        
        try:
            prompt = f"""
            Analyze this resume content for ATS (Applicant Tracking System) compatibility.
            Provide scores and suggestions in JSON format.
            
            Resume Content:
            {json.dumps(resume_content)}
            
            Return a JSON object with:
            - overall_score (0-100)
            - keyword_match (0-100)
            - grammar_score (0-100)
            - formatting_score (0-100)
            - action_verb_score (0-100)
            - missing_skills (list of strings)
            - suggestions (list of improvement suggestions)
            - section_analysis (list of objects with section and feedback)
            """
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Error in ATS analysis: {e}")
            return self._mock_ats_analysis()
    
    async def match_job_description(self, resume_content: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Match resume with job description."""
        if not self.client:
            return self._mock_job_matching()
        
        try:
            prompt = f"""
            Compare this resume with the job description and provide a match analysis.
            Return a JSON object with the analysis.
            
            Resume Content:
            {json.dumps(resume_content)}
            
            Job Description:
            {job_description}
            
            Return a JSON object with:
            - match_percentage (0-100)
            - matched_keywords (list of keywords found in both)
            - missing_keywords (list of important keywords missing from resume)
            - suggestions (list of improvement suggestions)
            """
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Error in job matching: {e}")
            return self._mock_job_matching()
    
    def _mock_ats_analysis(self) -> Dict[str, Any]:
        """Return mock ATS analysis for testing."""
        return {
            "overall_score": 72,
            "keyword_match": 75,
            "grammar_score": 85,
            "formatting_score": 70,
            "action_verb_score": 68,
            "missing_skills": ["Machine Learning", "AWS", "Docker"],
            "suggestions": [
                "Add more quantifiable achievements",
                "Include technical certifications",
                "Improve formatting consistency",
                "Add more industry keywords",
            ],
            "section_analysis": [
                {"section": "Skills", "score": 75, "feedback": ["Good variety of skills"]},
                {"section": "Experience", "score": 70, "feedback": ["Add more metrics and impact"]},
                {"section": "Education", "score": 85, "feedback": ["Well formatted"]},
            ],
        }
    
    def _mock_job_matching(self) -> Dict[str, Any]:
        """Return mock job matching for testing."""
        return {
            "match_percentage": 68,
            "matched_keywords": [
                "Python", "FastAPI", "MongoDB", "REST API",
                "Docker", "AWS", "Git"
            ],
            "missing_keywords": [
                "Kubernetes", "Microservices", "GraphQL",
                "PostgreSQL", "Redis"
            ],
            "suggestions": [
                "Consider learning Kubernetes for better match",
                "Emphasize your REST API experience more",
                "Add GraphQL experience if possible",
            ],
        }
