from src.services.celery import celery

import time
import datetime


@celery.task(name="create_task")
def create_task(delay):
    print(f'init: {datetime.datetime.utcnow().time()}')
    time.sleep(delay)
    print(f'end: {datetime.datetime.utcnow().time()}')
    return True
