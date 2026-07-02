"""Resume parsing and analysis service."""

import PyPDF2
from docx import Document
from typing import Dict, Any
import re
from app.utils.logger import logger


class ResumeService:
    """Service for parsing resume files."""
    
    def __init__(self, db):
        self.db = db
    
    async def parse_resume(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse resume file and extract content."""
        try:
            if file_ext == "pdf":
                return await self._parse_pdf(file_path)
            elif file_ext == "docx":
                return await self._parse_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            raise
    
    async def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF resume."""
        text = ""
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise
        
        return self._extract_resume_fields(text)
    
    async def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Extract text from DOCX resume."""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"Error reading DOCX: {e}")
            raise
        
        return self._extract_resume_fields(text)
    
    def _extract_resume_fields(self, text: str) -> Dict[str, Any]:
        """Extract structured fields from resume text."""
        return {
            "raw_text": text,
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience_years(text),
            "education": self._extract_education(text),
        }
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text."""
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text."""
        pattern = r"\+?1?\d{9,15}"
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    def _extract_skills(self, text: str) -> list:
        """Extract common skills from resume."""
        common_skills = [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#",
            "React", "Vue", "Angular", "Node.js", "FastAPI", "Django",
            "MongoDB", "PostgreSQL", "MySQL", "AWS", "Azure", "Docker",
            "Kubernetes", "Git", "REST API", "GraphQL", "SQL",
            "HTML", "CSS", "Tailwind", "Bootstrap", "Jest", "Pytest",
            "Linux", "Windows", "Mac", "CI/CD", "DevOps"
        ]
        found_skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def _extract_experience_years(self, text: str) -> int:
        """Estimate years of experience."""
        pattern = r"(\d+)\s*(?:years?|yrs?)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return max([int(m) for m in matches])
        return 0
    
    def _extract_education(self, text: str) -> list:
        """Extract education information."""
        degrees = ["Bachelor", "Master", "PhD", "Associate", "Diploma"]
        education = []
        text_lower = text.lower()
        for degree in degrees:
            if degree.lower() in text_lower:
                education.append(degree)
        return education
