# 🧙‍♀️✨ The Secret Library of Magic ‍✨‍🧙‍♀️

## 🐉 Project Overview
The Secret Library of Magic is a fantasy-themed web application built with Django.  
It represents a hidden library that contains magical books, grimoires created from people, dragon lore, and powerful potions.

Each section of the library explores a different aspect of magic:

[Tutorial Here](https://github.com/Viktoria-Todorova/DjangoExam/blob/main/docs/Magic_library_tutorial.md)

- **Books** – records stored in the main catalog  
- **Grimoires** – magical tomes formed from human souls and memories  
- **Potions** – brewed potions with mystical effects  
- **Dragons** – ancient beings guarding forbidden knowledge  
- **Users** – librarians and visitors of the secret library  

---

## 📜 Project Structure
```
DjangoExam/
├── LibraryProject/      # Main Django project (settings, urls, wsgi, asgi)
├── catalog/             # Book catalog app
├── grimoire/            # Grimoires created from people
├── potions/             # Magical potions
├── dragons/             # Dragon records
├── circulation/         # Borrowing and returning logic
├── users/               # Authentication and profiles
├── templates/           # Global templates
├── static/              # CSS, images, fonts
├── media/               # Uploaded files
├── docs/                # Project documentation
└── manage.py
```


---

## 🔮 Main Features
- View and search magical books  
- View / Create grimoires
- Meet the dragons and get matched with one 
- Create and store magical potions  
- Borrow and return books  
- User authentication and roles (staff vs visitors)  
- Admin-only edit/deletion of books

---

## 🪶 Technologies Used
- Python 3  
- Django + Django REST Framework  
- PostgreSQL (production) / SQLite (optional local fallback)  
- Redis + Celery (async task processing)  
- HTML5 / CSS3  
- Django Templates  
- Django Class-Based Views  
- Docker & Docker Compose  
- Git / GitHub  

---

## 🪄 Setup Instructions

### Local Development with Docker

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Viktoria-Todorova/DjangoExam.git
   cd DjangoExam
   ```

2. **Create environment file:**
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and set your values (you can use defaults for local testing).

3. **Build and run with Docker:**
   ```bash
   docker-compose up --build
   ```
   This will:
   - Start PostgreSQL database
   - Start Redis server
   - Run Django migrations
   - Start Django app on `http://localhost:8000`
   - Start Celery worker for async tasks

4. **Create a superuser (optional, run in another terminal):**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

5. **Access the app:**
   - Main app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

6. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Traditional Setup

See [Project Setup Instructions](https://github.com/Viktoria-Todorova/DjangoExam/blob/main/docs/project_setup.md)

---

## 🌍 Deployed Application

The application is live at:  
**https://magiclibrary-eahrbfhaapbafvh5.switzerlandnorth-01.azurewebsites.net/**

---

## 🔑 Environment Variables

All configuration is handled via a `.env` file. Copy `.env.template` and fill in your values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False

# PostgreSQL
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=library_password
DB_HOST=localhost
DB_PORT=5432

# Celery / Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Allowed hosts & CSRF
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

> For local Docker-based setup, `DB_HOST` should be `postgres` and Redis URL should use `redis` as the hostname, as defined in `docker-compose.yml`.
