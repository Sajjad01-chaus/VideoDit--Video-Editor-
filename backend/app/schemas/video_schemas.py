from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoBase(BaseModel):
    filename: str
    duration: Optional[int] = None
    size_bytes: Optional[int] = None

class VideoCreate(VideoBase):
    file_path: str

class VideoOut(VideoBase):
    id: int
    uploaded_at: datetime
    file_path: Optional[str] = None

    class Config:
        orm_mode = True
