"""Analytics service for user and system analytics."""

from datetime import datetime
from bson import ObjectId
from typing import Dict, Any
from app.utils.logger import logger


class AnalyticsService:
    """Service for analytics and reporting."""
    
    def __init__(self, db):
        self.db = db
    
    async def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user analytics."""
        try:
            user_obj_id = ObjectId(user_id)
            
            # Get resume count
            total_resumes = await self.db.resumes.count_documents({"user_id": user_obj_id})
            
            # Get ATS analyses count
            analyses = await self.db.analyses.find({"user_id": user_obj_id}).to_list(None)
            resumes_analyzed = len(analyses)
            
            # Calculate average ATS score
            average_ats_score = 0.0
            if analyses:
                total_score = sum(a.get("overall_score", 0) for a in analyses)
                average_ats_score = total_score / len(analyses)
            
            # Get job matches count
            job_matches = await self.db.job_matches.find({"user_id": user_obj_id}).to_list(None)
            job_matches_performed = len(job_matches)
            
            # Get most common missing skills
            all_missing_skills = []
            for analysis in analyses:
                all_missing_skills.extend(analysis.get("missing_skills", []))
            
            from collections import Counter
            skill_counts = Counter(all_missing_skills)
            most_common_missing_skills = [skill for skill, count in skill_counts.most_common(5)]
            
            return {
                "total_resumes": total_resumes,
                "resumes_analyzed": resumes_analyzed,
                "average_ats_score": round(average_ats_score, 2),
                "job_matches_performed": job_matches_performed,
                "most_common_missing_skills": most_common_missing_skills,
            }
        except Exception as e:
            logger.error(f"Error getting user analytics: {e}")
            raise
    
    async def get_admin_analytics(self) -> Dict[str, Any]:
        """Get admin analytics."""
        try:
            # Get total users
            total_users = await self.db.users.count_documents({})
            
            # Get total resumes
            total_resumes = await self.db.resumes.count_documents({})
            
            # Get total analyses
            total_analyses = await self.db.analyses.count_documents({})
            
            # Get average ATS score
            analyses = await self.db.analyses.find({}).to_list(None)
            average_ats_score = 0.0
            if analyses:
                total_score = sum(a.get("overall_score", 0) for a in analyses)
                average_ats_score = total_score / len(analyses)
            
            # Get total job matches
            total_job_matches = await self.db.job_matches.count_documents({})
            
            return {
                "total_users": total_users,
                "total_resumes": total_resumes,
                "total_analyses": total_analyses,
                "average_ats_score": round(average_ats_score, 2),
                "total_job_matches": total_job_matches,
            }
        except Exception as e:
            logger.error(f"Error getting admin analytics: {e}")
            raise
