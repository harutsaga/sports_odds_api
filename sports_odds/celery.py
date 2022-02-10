from __future__ import absolute_import, unicode_literals

import os

from django.apps import apps

from celery import Celery

from .celerybeat_schedule import CELERYBEAT_SCHEDULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sports_odds.settings")

app = Celery('celery_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))