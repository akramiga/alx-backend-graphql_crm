import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')

# Load settings from Django, namespace = CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks inside tasks.py
app.autodiscover_tasks()
