import os
import shutil
from datetime import datetime
from bson import ObjectId
from fastapi import UploadFile
from app.utils.exceptions import NotFoundException, BadRequestException
from app.services.resume_service import ResumeService
from app.services.ai_service import AIService
from app.config import settings

class ResumeController:
    def __init__(self, db):
        self.db = db
        self.resume_service = ResumeService(db)
        self.ai_service = AIService()
    
    async def upload_resume(self, user_id: str, file: UploadFile):
        """Upload and parse resume."""
        # Validate file
        if not file.filename:
            raise BadRequestException("File name is required")
        
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.ALLOWED_FILE_TYPES:
            raise BadRequestException(f"File type .{file_ext} not allowed")
        
        # Create uploads directory
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{user_id}_{datetime.utcnow().timestamp()}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse resume
        parsed_content = await self.resume_service.parse_resume(file_path, file_ext)
        
        # Store in database
        resume_doc = {
            "user_id": ObjectId(user_id),
            "file_name": file.filename,
            "file_url": file_path,
            "parsed_content": parsed_content,
            "uploaded_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        result = await self.db.resumes.insert_one(resume_doc)
        
        return {
            "_id": str(result.inserted_id),
            "user_id": user_id,
            "file_name": file.filename,
            "file_url": file_path,
            "uploaded_at": resume_doc["uploaded_at"],
            "parsed_content": parsed_content,
            "created_at": resume_doc["created_at"],
            "updated_at": resume_doc["updated_at"],
        }
    
    async def get_resumes(self, user_id: str):
        """Get all user resumes."""
        resumes = await self.db.resumes.find(
            {"user_id": ObjectId(user_id)}
        ).sort("created_at", -1).to_list(None)
        
        return [
            {
                "_id": str(resume["_id"]),
                "user_id": user_id,
                "file_name": resume["file_name"],
                "file_url": resume["file_url"],
                "uploaded_at": resume["uploaded_at"],
                "parsed_content": resume.get("parsed_content"),
                "ats_score": resume.get("ats_score"),
                "created_at": resume["created_at"],
                "updated_at": resume["updated_at"],
            }
            for resume in resumes
        ]
    
    async def get_resume(self, resume_id: str, user_id: str):
        """Get specific resume."""
        resume = await self.db.resumes.find_one({
            "_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id)
        })
        
        if not resume:
            raise NotFoundException("Resume not found")
        
        return {
            "_id": str(resume["_id"]),
            "user_id": user_id,
            "file_name": resume["file_name"],
            "file_url": resume["file_url"],
            "uploaded_at": resume["uploaded_at"],
            "parsed_content": resume.get("parsed_content"),
            "ats_score": resume.get("ats_score"),
            "created_at": resume["created_at"],
            "updated_at": resume["updated_at"],
        }
    
    async def delete_resume(self, resume_id: str, user_id: str):
        """Delete resume."""
        resume = await self.db.resumes.find_one_and_delete({
            "_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id)
        })
        
        if not resume:
            raise NotFoundException("Resume not found")
        
        # Delete file
        if os.path.exists(resume["file_url"]):
            os.remove(resume["file_url"])
        
        # Delete associated analyses
        await self.db.analyses.delete_many({"resume_id": ObjectId(resume_id)})
        await self.db.job_matches.delete_many({"resume_id": ObjectId(resume_id)})
        
        return {"message": "Resume deleted successfully"}
    
    async def analyze_ats(self, resume_id: str, user_id: str):
        """Analyze resume for ATS compatibility."""
        resume = await self.db.resumes.find_one({
            "_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id)
        })
        
        if not resume:
            raise NotFoundException("Resume not found")
        
        # Generate ATS analysis
        ats_analysis = await self.ai_service.analyze_ats(resume.get("parsed_content", {}))
        
        # Store analysis
        analysis_doc = {
            "resume_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id),
            "overall_score": ats_analysis["overall_score"],
            "keyword_match": ats_analysis["keyword_match"],
            "grammar_score": ats_analysis["grammar_score"],
            "formatting_score": ats_analysis["formatting_score"],
            "action_verb_score": ats_analysis["action_verb_score"],
            "missing_skills": ats_analysis["missing_skills"],
            "suggestions": ats_analysis["suggestions"],
            "section_analysis": ats_analysis.get("section_analysis", []),
            "created_at": datetime.utcnow(),
        }
        
        result = await self.db.analyses.insert_one(analysis_doc)
        
        # Update resume with ATS score
        await self.db.resumes.update_one(
            {"_id": ObjectId(resume_id)},
            {"$set": {"ats_score": analysis_doc, "updated_at": datetime.utcnow()}}
        )
        
        return {
            "_id": str(result.inserted_id),
            "resume_id": resume_id,
            "overall_score": ats_analysis["overall_score"],
            "keyword_match": ats_analysis["keyword_match"],
            "grammar_score": ats_analysis["grammar_score"],
            "formatting_score": ats_analysis["formatting_score"],
            "action_verb_score": ats_analysis["action_verb_score"],
            "missing_skills": ats_analysis["missing_skills"],
            "suggestions": ats_analysis["suggestions"],
            "section_analysis": ats_analysis.get("section_analysis", []),
            "created_at": analysis_doc["created_at"],
        }
    
    async def match_job_description(self, resume_id: str, user_id: str, job_description: str):
        """Match resume with job description."""
        resume = await self.db.resumes.find_one({
            "_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id)
        })
        
        if not resume:
            raise NotFoundException("Resume not found")
        
        # Generate job matching analysis
        matching = await self.ai_service.match_job_description(
            resume.get("parsed_content", {}),
            job_description
        )
        
        # Store matching result
        match_doc = {
            "resume_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id),
            "job_description": job_description,
            "match_percentage": matching["match_percentage"],
            "matched_keywords": matching["matched_keywords"],
            "missing_keywords": matching["missing_keywords"],
            "suggestions": matching["suggestions"],
            "created_at": datetime.utcnow(),
        }
        
        result = await self.db.job_matches.insert_one(match_doc)
        
        return {
            "_id": str(result.inserted_id),
            "resume_id": resume_id,
            "job_description": job_description,
            "match_percentage": matching["match_percentage"],
            "matched_keywords": matching["matched_keywords"],
            "missing_keywords": matching["missing_keywords"],
            "suggestions": matching["suggestions"],
            "created_at": match_doc["created_at"],
        }
    
    async def get_ats_score(self, resume_id: str, user_id: str):
        """Get ATS score for resume."""
        analysis = await self.db.analyses.find_one({
            "resume_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id)
        }).sort("created_at", -1)
        
        if not analysis:
            raise NotFoundException("ATS analysis not found")
        
        return {
            "_id": str(analysis["_id"]),
            "resume_id": resume_id,
            "overall_score": analysis["overall_score"],
            "keyword_match": analysis["keyword_match"],
            "grammar_score": analysis["grammar_score"],
            "formatting_score": analysis["formatting_score"],
            "action_verb_score": analysis["action_verb_score"],
            "missing_skills": analysis["missing_skills"],
            "suggestions": analysis["suggestions"],
            "section_analysis": analysis.get("section_analysis", []),
            "created_at": analysis["created_at"],
        }
    
    async def get_job_matching(self, resume_id: str, user_id: str):
        """Get latest job matching result."""
        matching = await self.db.job_matches.find_one({
            "resume_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id)
        }).sort("created_at", -1)
        
        if not matching:
            raise NotFoundException("Job matching not found")
        
        return {
            "_id": str(matching["_id"]),
            "resume_id": resume_id,
            "job_description": matching["job_description"],
            "match_percentage": matching["match_percentage"],
            "matched_keywords": matching["matched_keywords"],
            "missing_keywords": matching["missing_keywords"],
            "suggestions": matching["suggestions"],
            "created_at": matching["created_at"],
        }
