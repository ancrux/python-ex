from celery import Celery
import time

app = Celery(
    'tasks',
    backend='rpc://172.16.33.111//',
    broker='amqp://guest@172.16.33.111/my_broker',
    )

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE = 'UTC',
    CELERY_ENABLE_UTC = True,
    )

@app.task
def add(x, y):
    time.sleep(5)
    return x + y
