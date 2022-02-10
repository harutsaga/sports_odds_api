from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    #Internal tasks
    # 'test_task': {
    #     'schedule': 30.0,
    #     'task': 'api.tasks.bethistory'
    # },
}
