from celery.schedules import crontab

BROKER_URL = 'amqp://guest@172.16.33.111/my_broker'
CELERY_RESULT_BACKEND = 'rpc://172.16.33.111//'

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# CELERYBEAT_MAX_LOOP_INTERVAL = 10 # same as: celery beat --max-interval=10
CELERYBEAT_SCHEDULE = {
    'my-cronjob': {
        'task': 'tasks.add',
        'schedule': crontab(minute='*/1'),
        'args': (1,2),
    },
}


