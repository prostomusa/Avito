import os

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Avito.settings')

app = Celery('Avito')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
	'T1': {
		'task': 'request.tasks.counter',
		'schedule': crontab(minute=0, hour='*/1'),
	},
}