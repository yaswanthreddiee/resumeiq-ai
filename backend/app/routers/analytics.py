from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user, get_admin_user
from app.database.mongo import get_db
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("")
async def get_user_analytics(current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get user analytics."""
    user_id = ObjectId(str(current_user["_id"]))
    
    # Get total resumes
    total_resumes = await db.resumes.count_documents({"user_id": user_id})
    
    # Get total analyses
    total_analyses = await db.analyses.count_documents({"user_id": user_id})
    
    # Get average ATS score
    avg_score_agg = await db.analyses.aggregate([
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": None, "avg_score": {"$avg": "$overall_score"}}}
    ]).to_list(1)
    average_ats_score = avg_score_agg[0]["avg_score"] if avg_score_agg else 0
    
    # Get score history (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    score_history = await db.analyses.find(
        {"user_id": user_id, "created_at": {"$gte": thirty_days_ago}}
    ).sort("created_at", 1).to_list(None)
    
    score_history_data = [
        {"date": score["created_at"].strftime("%Y-%m-%d"), "score": score["overall_score"]}
        for score in score_history
    ]
    
    # Get upload stats
    upload_stats_agg = await db.resumes.aggregate([
        {"$match": {"user_id": user_id, "created_at": {"$gte": thirty_days_ago}}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]).to_list(None)
    
    upload_stats_data = [
        {"date": stat["_id"], "count": stat["count"]}
        for stat in upload_stats_agg
    ]
    
    return {
        "total_resumes": total_resumes,
        "average_ats_score": average_ats_score,
        "total_analyses": total_analyses,
        "score_history": score_history_data,
        "upload_stats": upload_stats_data,
    }

@router.get("/admin/analytics")
async def get_admin_analytics(current_user = Depends(get_admin_user), db = Depends(get_db)):
    """Get admin analytics."""
    # Get total users
    total_users = await db.users.count_documents()
    
    # Get total resumes
    total_resumes = await db.resumes.count_documents()
    
    # Get total analyses
    total_analyses = await db.analyses.count_documents()
    
    # Get average ATS score
    avg_score_agg = await db.analyses.aggregate([
        {"$group": {"_id": None, "avg_score": {"$avg": "$overall_score"}}}
    ]).to_list(1)
    average_ats_score = avg_score_agg[0]["avg_score"] if avg_score_agg else 0
    
    # Get user growth (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    user_growth_agg = await db.users.aggregate([
        {"$match": {"created_at": {"$gte": thirty_days_ago}}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]).to_list(None)
    
    user_growth_data = [
        {"date": stat["_id"], "users": stat["count"]}
        for stat in user_growth_agg
    ]
    
    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "total_analyses": total_analyses,
        "average_ats_score": average_ats_score,
        "user_growth": user_growth_data,
    }
