import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_app.settings')

celery = Celery('movies_app')

celery.config_from_object('movies_app.celeryconfig')

# Load task modules from all registered Django app configs.
celery.autodiscover_tasks()
