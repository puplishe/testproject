import time
from datetime import timedelta

import requests
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('parsing')
app.conf.update(broker_url='amqp://guest:guest@rabbitmq:5672', broker_connection_retry_on_startup=True)
app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'parsing',
        'schedule': timedelta(seconds=15)
    },
}
# crontab(seconds='*/15')
celery_logger = get_task_logger(__name__)


@app.task(name='parsing')
def parse_excel_task():
    time.sleep(5)
    print('zalupa')
    celery_logger.info('parsing')
    requests.post('http://api:8000/api/v1/parser/parse-excel')
