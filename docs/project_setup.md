# 🧙‍♂️ Project Setup Instructions

Welcome to your **Magic Library** project! Follow these steps to get your wizarding environment ready. ✨

---

## ⚡ Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) & Docker Compose  
- [Git](https://git-scm.com/)  

---

## 🪄 Setup Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/Viktoria-Todorova/DjangoExam.git
cd DjangoExam
```

### Step 2: Configure Environment Variables

```bash
cp .env.template .env
```

Edit `.env` and fill in your values:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Use `postgres` for Docker |
| `DB_PORT` | `5432` |
| `CELERY_BROKER_URL` | Use `redis://redis:6379/0` for Docker |
| `CELERY_RESULT_BACKEND` | Use `redis://redis:6379/0` for Docker |
| `ALLOWED_HOSTS` | Comma-separated, e.g. `localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | e.g. `http://localhost:8000` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name for media storage |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |

### Step 3: Build and Run

```bash
docker-compose up --build
```

This starts:
- PostgreSQL database
- Redis server
- Django app on http://localhost:8000
- Celery worker for async tasks
- pgAdmin on http://localhost:5050

### Step 4: Create a Superuser

In a second terminal:

```bash
docker-compose exec django python manage.py createsuperuser
```

### Step 5: Access the App

| Service | URL |
|---------|-----|
| Main app | http://localhost:8000 |
| Admin panel | http://localhost:8000/admin |
| pgAdmin | http://localhost:5050 |

pgAdmin credentials: email `admin@admin.com`, password `admin`  
To connect pgAdmin to the DB use host `postgres`, port `5432`.

### Step 6: Stop the Application

```bash
docker-compose down
```

> ⚠️ If you run into database connection errors on a fresh start, run `docker-compose down -v` first to clear old volumes.

---

#### [← Back to README](../README.md) | [Magic Library Tutorial →](./Magic_library_tutorial.md)
