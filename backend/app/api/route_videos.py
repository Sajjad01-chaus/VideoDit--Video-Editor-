from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.db_session import SessionLocal
from app.services.storage import save_upload_file
from uuid import uuid4
from typing import List
from app.schemas.video_schemas import VideoCreate, VideoOut
from app.tasks.celery_tasks import task_trim, task_variants
import os
from app.services.video_processing import do_text_overlay, do_watermark, make_variants
from app.database import db_models
import subprocess, json


router = APIRouter(prefix="/videos", tags=["videos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", response_model=VideoOut)
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = save_upload_file(file)
    size = os.path.getsize(path)

    duration = None
    try:
        cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams "{path}"'
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        
        if proc.returncode == 0 and proc.stdout:
            stdout_str = proc.stdout.decode().strip()
            if stdout_str:
                info = json.loads(stdout_str)
                if 'format' in info and 'duration' in info['format']:
                    duration = int(float(info['format']['duration']))
    except Exception as e:
        print(f"Error getting video duration: {e}")
    v = db_models.Video(filename=file.filename, file_path=path, duration=duration, size_bytes=size)
    db.add(v); db.commit(); db.refresh(v)
    return {"id": v.id, "filename": v.filename, "duration": v.duration, "size_bytes": v.size_bytes, "uploaded_at": v.uploaded_at, "file_path": v.file_path}

@router.get("/", response_model=List[VideoOut])
def list_videos(limit: int=50, db: Session = Depends(get_db)):
    vids = db.query(db_models.Video).order_by(db_models.Video.uploaded_at.desc()).limit(limit).all()
    return vids

@router.post("/trim")
def trim_endpoint(video_id: int, start: float, end: float, db: Session = Depends(get_db)):
    video = db.query(db_models.Video).get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="video not found")
    job_id = uuid4().hex
    job = db_models.Job(id=job_id, status=db_models.JobStatus.PENDING, type="trim", video_id=video.id)
    db.add(job); db.commit()
    # enqueue celery
    task_trim.delay(job_id, video.file_path, start, end)
    return {"job_id": job_id}



@router.post("/{video_id}/overlay/text", response_model=VideoOut)
def add_text_overlay(
    video_id: int,
    text: str,
    db: Session = Depends(get_db)
):
    video = db.query(db_models.Video).filter(db_models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Process video with text overlay
    output_file = do_text_overlay(video.file_path, text, "Arial.ttf", start=0, end=5)

    new_video = db_models.Video(
        filename=f"text_overlay_{video.filename}",
        file_path=output_file,
        parent_id=video.id
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return new_video

@router.post("/{video_id}/watermark", response_model=VideoOut)
def add_watermark(
    video_id: int,
    watermark_path: str,
    db: Session = Depends(get_db)
):
    video = db.query(db_models.Video).filter(db_models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Process video with watermark
    output_file = do_watermark(video.file_path, watermark_path)

    new_video = db_models.Video(
        filename=f"watermarked_{video.filename}",
        file_path=output_file,
        parent_id=video.id
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return new_video


@router.post("/{video_id}/variants")
def generate_variants(video_id: int, db: Session = Depends(get_db)):
    video = db.query(db_models.Video).filter(db_models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    variants = make_variants(video, video.file_path)
    return variants