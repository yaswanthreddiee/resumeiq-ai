import re


class ResumeParser:
    """
    Extract structured information from resume text.
    """

    async def parse(self, raw_text: str):

        return {
            "raw_text": raw_text,
            "email": self._extract_email(raw_text),
            "phone": self._extract_phone(raw_text),
            "skills": self._extract_skills(raw_text),
            "education": self._extract_education(raw_text),
            "experience": self._extract_experience(raw_text),
        }

    def _extract_email(self, text: str):
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        match = re.search(pattern, text)

        return match.group(0) if match else ""

    def _extract_phone(self, text: str):
        pattern = r"\+?\d[\d\s-]{8,15}"

        match = re.search(pattern, text)

        return match.group(0) if match else ""

    def _extract_skills(self, text: str):

        skills = [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "React",
            "Node.js",
            "FastAPI",
            "Django",
            "MongoDB",
            "MySQL",
            "PostgreSQL",
            "Git",
            "Docker",
            "HTML",
            "CSS",
            "AWS",
        ]

        found = []

        lower = text.lower()

        for skill in skills:
            if skill.lower() in lower:
                found.append(skill)

        return found

    def _extract_education(self, text: str):

        education = []

        keywords = [
            "Bachelor",
            "Master",
            "B.Tech",
            "M.Tech",
            "B.E",
            "M.E",
            "Diploma",
            "PhD",
        ]

        lower = text.lower()

        for item in keywords:
            if item.lower() in lower:
                education.append(item)

        return education

    def _extract_experience(self, text: str):

        pattern = r"(\d+)\s*(?:years?|yrs?)"

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        if matches:
            return max(int(x) for x in matches)

        return 0