from celery import Celery
from app.core.config import BROKER_URL, REDIS_URL, MEDIA_ROOT
from pathlib import Path
from app.services.video_processing import do_trim, make_variants
from app.database.db_session import SessionLocal
from app.database import db_models
import uuid
from sqlalchemy import update

cel = Celery("worker", broker=BROKER_URL, backend=REDIS_URL)
cel.conf.task_serializer = "json"

@cel.task(bind=True)
def task_trim(self, job_id, input_path, start, end):
    db = SessionLocal()
    try:
        # update job status to RUNNING
        db.query(models.Job).filter(models.Job.id == job_id).update({"status": models.JobStatus.RUNNING})
        db.commit()
        out = do_trim(input_path, start, end)
        # update job row
        db.query(models.Job).filter(models.Job.id == job_id).update({"status": models.JobStatus.SUCCESS, "result_path": out})
        db.commit()
        return {"result": out}
    except Exception as e:
        db.query(models.Job).filter(models.Job.id == job_id).update({"status": models.JobStatus.FAILED, "meta": {"error": str(e)}})
        db.commit()
        raise
    finally:
        db.close()

@cel.task(bind=True)
def task_variants(self, job_id, input_path):
    db = SessionLocal()
    try:
        db.query(models.Job).filter(models.Job.id == job_id).update({"status": models.JobStatus.RUNNING})
        db.commit()
        variants = make_variants(input_path)
        # store variants info in DB
        for q,path in variants.items():
            v = models.VideoVersion(video_id=None, quality=q, filepath=path, size_bytes=Path(path).stat().st_size)
            db.add(v)
        db.query(models.Job).filter(models.Job.id == job_id).update({"status": models.JobStatus.SUCCESS, "result_path": str(variants)})
        db.commit()
        return {"result": variants}
    except Exception as e:
        db.query(models.Job).filter(models.Job.id == job_id).update({"status": models.JobStatus.FAILED, "meta": {"error": str(e)}})
        db.commit()
        raise
    finally:
        db.close()
