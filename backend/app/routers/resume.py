from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse
from app.controllers.resume_controller import ResumeController
from app.middleware.auth import get_current_user
from app.database.mongo import get_db
from app.schemas.schemas import JobDescriptionSchema

router = APIRouter(prefix="/api/resumes", tags=["resumes"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Upload and parse resume."""
    controller = ResumeController(db)
    return await controller.upload_resume(str(current_user["_id"]), file)

@router.get("")
async def get_resumes(current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get all user resumes."""
    controller = ResumeController(db)
    return await controller.get_resumes(str(current_user["_id"]))

@router.get("/{resume_id}")
async def get_resume(resume_id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get specific resume."""
    controller = ResumeController(db)
    return await controller.get_resume(resume_id, str(current_user["_id"]))

@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    """Delete resume."""
    controller = ResumeController(db)
    return await controller.delete_resume(resume_id, str(current_user["_id"]))

@router.post("/{resume_id}/analyze-ats")
async def analyze_ats(resume_id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    """Analyze resume for ATS compatibility."""
    controller = ResumeController(db)
    return await controller.analyze_ats(resume_id, str(current_user["_id"]))

@router.post("/{resume_id}/match-job")
async def match_job_description(
    resume_id: str,
    data: JobDescriptionSchema,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Match resume with job description."""
    controller = ResumeController(db)
    return await controller.match_job_description(resume_id, str(current_user["_id"]), data.job_description)

@router.get("/{resume_id}/ats-score")
async def get_ats_score(resume_id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get ATS score for resume."""
    controller = ResumeController(db)
    return await controller.get_ats_score(resume_id, str(current_user["_id"]))

@router.get("/{resume_id}/job-matching")
async def get_job_matching(resume_id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get latest job matching result."""
    controller = ResumeController(db)
    return await controller.get_job_matching(resume_id, str(current_user["_id"]))
