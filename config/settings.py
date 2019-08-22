# -*- coding: utf-8 -*-
from datetime import timedelta
import os
from celery.schedules import crontab

DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = None
SECRET_KEY = 'water@dnp'
TOKEN_PREFIX = "TOKEN"

# Flask-Babel.
LANGUAGES = {
    'vn': u'Tiếng Việt',
    'en': 'English',
}
BABEL_DEFAULT_LOCALE = 'vn'

# Celery.
BROKER_POOL_LIMIT = None
# CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL', 'amqp://rabbitmq:rabbitmq@10.0.0.32:5672')
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
CELERYBEAT_SCHEDULE = {
    'celery-tasks': {
        'task': 'mrsservice.blueprints.route.tasks.transaction_event',
        # Every 60s
        'schedule': 60,
    }
}
# Redis
REDIS_URL = 'redis://:devpassword@redis'
REDIS_HOST = 'redis'
REDIS_PORT = 6379
ODOO_URL = os.environ.get('ODOO_URL', 'https://dtw-management-core-8eec1e97-odoo.dnpsoftware.vn')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'ns3.dnpwater@gmail.com'
MAIL_PASSWORD = 'zaq1@2wsx#'
MAIL_SUPPRESS_SEND = False
MAIL_DEFAULT_SENDER = 'ns3.dnpwater@gmail.com'
MAIL_DEFAULT_MS3_ADMIN = ['do.tran@dnpcorp.vn']
CLOUDINARY_URL = "cloudinary: // 851844615293399:Rxglnpv8YVypqUkm4GOE4ZPW1JM@dnp"
