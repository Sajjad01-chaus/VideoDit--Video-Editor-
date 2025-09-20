from app.core.ffmpeg_utils import trim_video, add_image_watermark, add_text_overlay, transcode_quality
from pathlib import Path
from app.core.config import MEDIA_ROOT
from app.database.db_session import SessionLocal
from app.database.db_models import VideoVersion
import os


def do_trim(input_path, start, end, out_sub="trims"):
    out_dir = Path(MEDIA_ROOT) / out_sub
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"trim_{Path(input_path).stem}_{start}_{end}.mp4"
    trim_video(input_path, str(out_path), start, end)
    return str(out_path)


def do_watermark(input_path, watermark_path, out_sub="watermarks"):
    out_dir = Path(MEDIA_ROOT) / out_sub
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"wm_{Path(input_path).stem}.mp4"
    add_image_watermark(input_path, watermark_path, str(out_path))
    return str(out_path)


def do_text_overlay(input_path, text, fontfile, start, end, out_sub="overlays"):
    out_dir = Path(MEDIA_ROOT) / out_sub
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"txt_{Path(input_path).stem}.mp4"
    add_text_overlay(input_path, str(out_path), text, fontfile, start=start, end=end)
    return str(out_path)


def make_variants(video, input_path):
    """
    Create multiple quality variants and save them in DB.
    :param video: parent Video object (must have .id)
    :param input_path: original video path
    :return: dict {quality: path}
    """
    out = {}
    mapping = {
        "1080p": "1920x1080",
        "720p": "1280x720",
        "480p": "854x480"
    }

    db = SessionLocal()
    try:
        for q, res in mapping.items():
            out_path = Path(MEDIA_ROOT) / "variants" / f"{Path(input_path).stem}_{q}.mp4"
            out_path.parent.mkdir(parents=True, exist_ok=True)

            # transcode
            transcode_quality(input_path, str(out_path), res)
            out[q] = str(out_path)

            # ✅ Save in DB with correct video_id
            variant = VideoVersion(
                video_id=video.id,
                quality=q,
                filepath=str(out_path),
                size_bytes=os.path.getsize(out_path),
            )
            db.add(variant)

        db.commit()
    finally:
        db.close()

    return out
