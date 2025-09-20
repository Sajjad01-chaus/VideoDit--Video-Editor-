from sqlalchemy import Column, Integer, String, DateTime, JSON, BigInteger, Boolean, Enum
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import ForeignKey

Base= declarative_base()

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key= True, index= True)
    filename= Column(String, nullable= False)
    file_path= Column(String, nullable= False)
    duration= Column(Integer)
    size_bytes= Column(BigInteger)
    uploaded_at= Column(DateTime, server_default=func.now())


class VideoVersion(Base):
    __tablename__ = "video_versions"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"))
    quality = Column(String, nullable=False)  # "1080p", "720p", "480p"
    filepath = Column(String, nullable=False)
    size_bytes = Column(BigInteger)
    created_at = Column(DateTime, server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)  # use UUID or celery task id
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    type = Column(String)  # e.g., "trim", "overlay", "encode_variants"
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    result_path = Column(String, nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

