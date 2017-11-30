from ConfigParser import SafeConfigParser
from flask import Flask
from celery import Celery
from flask_restful import Api
from kombu.common import Broadcast, Queue

app = Flask(__name__)

config = SafeConfigParser()
config.read('config.ini')

app.config['broker_url'] = config.get("Default", "CELERY_BROKER_URL")
app.config['result_backend'] = config.get("Default", "CELERY_RESULT_BACKEND")
app.config['tasks'] = config.get("Default", "APPLICATION_TASKS")
app.config['result_timeout'] = config.get("Default", "PERSIST_RESULTS")

api = Api(app)
celery = Celery(app.name, broker=app.config['broker_url'],
                backend=app.config['result_backend'], include=app.config['tasks'])
celery.conf.update(
    result_expires=int(app.config['result_timeout']),
)
celery.conf.task_queues = (Broadcast('broadcast_tasks'), Queue('default', routing_key='task.#'),)

celery.conf.update(app.config)

import core.runner
import core.status
import core.output
