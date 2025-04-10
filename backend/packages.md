# 📦 Python Packages for Django Project

This project uses Django with essential packages for API development, background tasks, security, media handling, CSP security, and optional content streaming support. Below is a complete guide for setting up your environment.

---

## ✅ Install Core Required Packages

Run this in your virtual environment to install the essential packages:

```bash
pip install django python-decouple whitenoise django-celery-beat django-celery-results django-storages django-cors-headers djangorestframework djangorestframework-simplejwt django-filter django-sqids google-api-python-client pillow redis django-summernote psycopg2-binary gunicorn
```

##  🔒 Install CSP Required Packages (This is a Must)
```bash
pip install -U django-csp
```

##  🧪 Optional: StreamField (if Needed)
```bash
pip install django-streamfield
```
