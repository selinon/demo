import os

BROKER_URL = os.environ.get('BROKER_URL', 'amqp://broker:5672')
CELERY_RESULT_BACKEND = os.environ.get('RESULT_BACKEND_URL', 'redis://redis:6379/0')

CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
