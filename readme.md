🐳 Django + Celery + Redis + PostgreSQL + PgAdmin + Nginx (Dockerized)

This is a production-ready, Dockerized Django application setup with PostgreSQL, Redis, Celery, PgAdmin, and Nginx.  
It also supports running in environments with or without Docker (e.g., VPS with venv or cPanel setups).

▶️ Django Backend + Nginx:

```bash
docker-compose up
```

▶️ Django + Celery Worker

```bash
docker-compose --profile celery up
```

▶️ Next.js Frontend + Django API

```bash
docker-compose --profile nextjs up
```

▶️ Next.js Frontend + Django API + Celery Worker

```bash
docker-compose --profile nextjs --profile celery up
```

📦 Services Overview

- Django App: Gunicorn-based backend (in /backend)
- PostgreSQL: Relational database for Django
- Redis: Message broker for Celery
- PgAdmin4: Web-based PostgreSQL admin
- Celery: Background task processor
- Nginx: Reverse proxy for Django app
- Volumes: Persistent data for PostgreSQL and static files

🚀 Getting Started (Docker)

1. Build and Run the Containers

   docker-compose build
   docker-compose up -d

2. Access Django Container Shell

   docker exec -it django_app /bin/bash

   # or

   docker exec -it django_app sh

3. Start a New Django App (one-time)

   docker-compose run django_app sh -c "django-admin startapp newapp ."

4. Collect Static Files

   docker-compose exec django_app python manage.py collectstatic

🧠 PgAdmin4 Access

To find the container IP for setting up a new PgAdmin server:

    docker ps
    docker inspect <container_id_or_prefix>

Then use:

- Email: root@root.com
- Password: root

Connect using the internal host (e.g., postgres_db) and port 5432.

🌍 Nginx Access

Once up, your Django app will be accessible at:
http://localhost or your server's IP address.

🛠 Flexible Deployment

This setup is designed to work both:

- As a fully containerized system (ideal for VPS or CI/CD environments)
- In manual environments like cPanel or virtualenv (by directly running Django with venv)

📁 Project Structure

project-root/
│
├── backend/ # Django source code
├── nginx/ # Nginx config (nginx-setup.conf)
├── data/ # PostgreSQL volume
├── docker-compose.yml
├── .env.sample # .env for Cpanel shared host passenger_wsgi
├── passenger_wsgi.py # application entry point for Cpanel

✅ Requirements

- Docker & Docker Compose installed
- Basic understanding of Django and Docker

Feel free to contribute or modify for your own deployment workflow!
