from pathlib import Path
import shutil
import os 
from uuid import uuid4
from app.core.config import MEDIA_ROOT

Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)

def save_upload_file(upload_file, sub_dir="uploads"):
    ext= Path(upload_file.filename).suffix
    file_name= f"{uuid4()}{ext}"
    dest_dir= Path(MEDIA_ROOT) / sub_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path= dest_dir / file_name
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return str(dest_path)
    
