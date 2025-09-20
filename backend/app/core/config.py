import os

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:postgres@db:5432/postgres")
REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/0")
BROKER_URL = os.getenv("BROKER_URL", REDIS_URL)
FFMPEG_PATH = os.getenv("FFMPEG_PATH","ffmpeg")
FFPROBE_PATH = os.getenv("FFPROBE_PATH","ffprobe")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "/data/media")