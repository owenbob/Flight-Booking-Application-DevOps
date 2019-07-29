from celery.schedules import crontab


CELERY_IMPORTS = ('api.celery.celery_tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'email-reminder-celery': {
        'task': 'api.celery.celery_tasks.send_reminder',
        # Execute Everyday at midnight
        'schedule': crontab(minute=0, hour=0),
    }
}
