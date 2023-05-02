import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo_notes.settings')

app = Celery('fundoo_notes')

app.conf.enable_utc = False

# app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


