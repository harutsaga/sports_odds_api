celery -A sports_odds beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler