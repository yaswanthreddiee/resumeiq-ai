import PyPDF2
from docx import Document
from typing import Dict, List, Any

class ResumeService:
    def __init__(self, db):
        self.db = db
    
    async def parse_resume(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Parse resume from PDF or DOCX."""
        if file_type == "pdf":
            return self._parse_pdf(file_path)
        elif file_type == "docx":
            return self._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF."""
        text = ""
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        
        return self._extract_sections(text)
    
    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Extract text from DOCX."""
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
        
        return self._extract_sections(text)
    
    def _extract_sections(self, text: str) -> Dict[str, Any]:
        """Extract resume sections from text."""
        # Basic extraction - can be enhanced with NLP
        sections = {
            "summary": self._extract_summary(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "education": self._extract_education(text),
            "projects": [],
            "certifications": [],
        }
        return sections
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary."""
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if "summary" in line.lower() or "objective" in line.lower():
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills."""
        skills = []
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if "skills" in line.lower():
                # Extract next few lines as skills
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip() and not any(keyword in lines[j].lower() for keyword in ["experience", "education", "projects"]):
                        skill_items = [s.strip() for s in lines[j].split(",")]
                        skills.extend([s for s in skill_items if s])
        return list(set(skills))
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience."""
        return []
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education."""
        return []
