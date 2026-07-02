from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Auth Schemas
class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: str
    name: str
    role: str = "user"
    created_at: datetime
    updated_at: datetime

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserSchema

# Resume Schemas
class ResumeParsedContentSchema(BaseModel):
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []
    education: List[dict] = []
    projects: List[dict] = []
    certifications: List[dict] = []

class ResumeSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    file_name: str
    file_url: str
    uploaded_at: datetime
    parsed_content: Optional[ResumeParsedContentSchema] = None
    ats_score: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

# ATS Score Schema
class ATSScoreSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    resume_id: str
    overall_score: float
    keyword_match: float
    grammar_score: float
    formatting_score: float
    action_verb_score: float
    missing_skills: List[str] = []
    suggestions: List[str] = []
    section_analysis: List[dict] = []
    created_at: datetime

# Job Matching Schema
class JobMatchingSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    resume_id: str
    job_description: str
    match_percentage: float
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []
    suggestions: List[str] = []
    created_at: datetime

class JobDescriptionSchema(BaseModel):
    job_description: str = Field(min_length=10)
