"""Pydantic models for request/response validation."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserSignupSchema(BaseModel):
    """User signup request."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class UserLoginSchema(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    """User response."""
    _id: str
    email: str
    name: str
    role: str
    created_at: datetime
    updated_at: datetime


class TokenResponseSchema(BaseModel):
    """Token response."""
    access_token: str
    token_type: str
    user: UserResponseSchema


class UpdateProfileSchema(BaseModel):
    """Update profile request."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ResumeUploadSchema(BaseModel):
    """Resume upload response."""
    _id: str
    user_id: str
    file_name: str
    file_url: str
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime


class ResumeParsedContent(BaseModel):
    """Parsed resume content."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[List[dict]] = []
    education: Optional[List[dict]] = []
    skills: Optional[List[str]] = []
    certifications: Optional[List[str]] = []
    projects: Optional[List[dict]] = []


class ATSAnalysisSchema(BaseModel):
    """ATS analysis response."""
    _id: str
    resume_id: str
    overall_score: float
    keyword_match: float
    grammar_score: float
    formatting_score: float
    action_verb_score: float
    missing_skills: List[str]
    suggestions: List[str]
    section_analysis: Optional[List[dict]] = []
    created_at: datetime


class JobMatchingSchema(BaseModel):
    """Job matching response."""
    _id: str
    resume_id: str
    job_description: str
    match_percentage: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
    created_at: datetime


class JobDescriptionMatchRequestSchema(BaseModel):
    """Job description matching request."""
    job_description: str = Field(..., min_length=10)


class AnalyticsResponseSchema(BaseModel):
    """Analytics response."""
    total_resumes: int
    average_ats_score: float
    resumes_analyzed: int
    job_matches_performed: int
    most_common_missing_skills: List[str]
