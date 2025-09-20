# 🎬 VideoDit – Video Processing Platform

VideoDit is a **video editing & processing backend service** built with **FastAPI**, **Celery**, and **PostgreSQL**, packaged with **Docker** for easy deployment.  
It supports core features like:

- Uploading videos
- Trimming
- Adding text overlay
- Adding watermark
- Generating multiple quality variants (1080p, 720p, 480p)
- Tracking jobs with Celery
- Serving media via FastAPI static files
- Simple **Streamlit frontend** for testing/demo

---

## 🚀 Tech Stack

- **Backend:** FastAPI + SQLAlchemy + Alembic  
- **Database:** PostgreSQL  
- **Queue:** Redis + Celery workers  
- **Media processing:** ffmpeg / ffprobe  
- **Frontend:** Streamlit (demo client)  
- **Containerization:** Docker & Docker Compose  
- **Tests:** pytest  

---

## ⚙️ Project Structure

backend/
├── app/
│ ├── api/ # FastAPI routes (videos, jobs)
│ ├── core/ # Config & ffmpeg utils
│ ├── database/ # DB models & session
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic (storage, video_processing)
│ ├── tasks/ # Celery async tasks
│ └── main.py # FastAPI entrypoint
├── alembic/ # DB migrations
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
frontend/
└── app.py # Streamlit demo UI

---

## 🔧 Setup & Running

### 1️⃣ Clone repo
```bash
git clone https://github.com/<your-username>/videodit.git
cd videodit
```
### 2️⃣ Build containers
docker compose build

### 3️⃣ Run stack
docker compose up


## Services started:

FastAPI backend → http://localhost:8000

Redis → localhost:6379

Postgres → localhost:5432

Celery worker → auto-starts with docker compose

Streamlit frontend → run locally (see below)

## 🗄 Database Migration

To init DB schema:
```
docker compose exec web alembic revision --autogenerate -m "init schema"
docker compose exec web alembic upgrade head
```
## 📡 API Endpoints

POST /videos/upload → Upload MP4

GET /videos/ → List uploaded videos

POST /videos/{video_id}/trim?start=..&end=.. → Trim

POST /videos/{video_id}/overlay/text?text=Hello → Text overlay

POST /videos/{video_id}/watermark → Add watermark

POST /videos/{video_id}/variants → Generate quality variants

### ▶️ Jobs

GET /jobs/{job_id} → Check Celery job status


## 🖥 Frontend (Streamlit Demo)

Run Streamlit UI:
```
cd frontend
streamlit run app.py
```

<img src="./Screenshot 2025-09-20 224317.png" alt="drawing" width="200"/>




## 🧪 Tests

Run unit tests with pytest:
```
docker compose exec web pytest -v
```


## 🏗 Future Improvements

Add authentication (JWT)

Support subtitles / audio extraction

Real-time processing progress

Deploy on AWS/GCP with CI/CD

## 👨‍💻 Authors

Built by Sajjad
