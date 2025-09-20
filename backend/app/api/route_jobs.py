from fastapi import APIRouter, Depends, HTTPException
from app.api.route_videos import get_db
from app.database import db_models

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/status/{job_id}")
def job_status(job_id: str, db=Depends(get_db)):
    job = db.query(models.Job).get(job_id)
    if not job:
        raise HTTPException(404, "job not found")
    return {"job_id": job.id, "status": job.status, "result_path": job.result_path, "meta": job.meta}

@router.get("/result/{job_id}")
def job_result(job_id: str, db=Depends(get_db)):
    job = db.query(models.Job).get(job_id)
    if not job:
        raise HTTPException(404, "job not found")
    if job.status != models.JobStatus.SUCCESS:
        raise HTTPException(400, "job not complete")
    return {"result_path": job.result_path}
