import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boardproj.settings')

app = Celery('boardapp')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_sunday_11am': {
        'task': 'board.tasks.weekly_news',
        #'schedule': crontab(),
        'schedule': crontab(hour=11, minute=0, day_of_week='sunday'),
        'args': (),
    },
}
