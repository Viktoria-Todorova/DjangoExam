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
- Django  
- SQLite (development)  
- HTML5 / CSS3  
- Django Templates  
- Django Class-Based Views  
- Git  

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
