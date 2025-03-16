import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Load task modules from all registered Django apps
app.config_from_object("django.conf:settings", namespace="CELERY")

# app.conf.update(
#     CELERY_TASK_ALWAYS_EAGER=True,  # Optional, runs tasks locally instead of in the background
#     CELERYD_POOL = 'solo'  # Uses solo pool for Windows, avoids multiprocessing
# )

app.autodiscover_tasks()

# from django.conf import settings
# Apply Eager Mode in Development
# if settings.DEBUG:
#     app.conf.task_always_eager = True
#     app.conf.task_eager_propagates = True
    
# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")

