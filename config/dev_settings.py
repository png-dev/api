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
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
CELERYBEAT_SCHEDULE = {

}
# Redis
REDIS_URL = 'redis://localhost'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
ODOO_URL = os.environ.get('ODOO_URL', 'http://192.168.100.4:8069')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'ns3.dnpwater@gmail.com'
MAIL_PASSWORD = 'zaq1@2wsx#'
MAIL_SUPPRESS_SEND = False
MAIL_DEFAULT_SENDER = 'ns3.dnpwater@gmail.com'
MAIL_DEFAULT_MS3_ADMIN = ['do.tran@dnpcorp.vn']
