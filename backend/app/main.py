from fastapi import FastAPI
from app.api import route_videos, route_jobs
from app.database.db_session import engine
from app.database.db_models import Base
from app.core.config import MEDIA_ROOT
from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(route_videos.router, prefix="/api")
app.include_router(route_jobs.router, prefix="/api")

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")