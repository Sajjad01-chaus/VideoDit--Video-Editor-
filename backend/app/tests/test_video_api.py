import os
import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_session import SessionLocal
from app.models.video import Video, VideoVersion

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Clear DB before each test"""
    db = SessionLocal()
    db.query(VideoVersion).delete()
    db.query(Video).delete()
    db.commit()
    db.close()
    yield


def test_upload_video(tmp_path):
    """Test uploading a video creates DB entry"""
    # create dummy file
    file_path = tmp_path / "test.mp4"
    with open(file_path, "wb") as f:
        f.write(os.urandom(1024))  # random bytes

    with open(file_path, "rb") as f:
        response = client.post(
            "/videos/upload",
            files={"file": ("test.mp4", f, "video/mp4")},
        )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "filename" in data
    assert data["filename"] == "test.mp4"


def test_trim_video(tmp_path):
    """Test trimming a video returns new video"""
    # Step 1: upload a video
    file_path = tmp_path / "test.mp4"
    with open(file_path, "wb") as f:
        f.write(os.urandom(2048))

    with open(file_path, "rb") as f:
        upload = client.post(
            "/videos/upload",
            files={"file": ("test.mp4", f, "video/mp4")},
        )
    video_id = upload.json()["id"]

    # Step 2: trim API
    response = client.post(
        f"/videos/{video_id}/trim",
        json={"start": 0, "end": 1},
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "filepath" in data
    assert os.path.exists(data["filepath"])
