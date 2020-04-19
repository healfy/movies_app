import os
from kombu import Exchange, Queue
from django.conf import settings

env = os.environ
broker_url = env.get('CELERY_BROKER_URL',
                     'amqp://admin:mypass@celery-rabbitmq:5673')
result_backend = env.get('CELERY_RESULT_BACKEND', broker_url)
timezone = settings.TIME_ZONE

task_default_exchange = Exchange('default')
task_download_exchange = Exchange('download')

task_default_queue = Queue(
    task_default_exchange.name, task_default_exchange,
    routing_key=task_default_exchange.name
)

task_download_queue = Queue(
    task_download_exchange.name, task_download_exchange,
    routing_key=task_download_exchange.name
)

task_queues = (
    task_default_queue,
    task_download_queue,
)
task_ignore_result = True

task_routes = {
    'movies.tasks.convert_video': {
        'queue': task_default_queue.name
    },
    'movies.tasks.download_video': {
        'queue': task_download_queue.name
    },
}
