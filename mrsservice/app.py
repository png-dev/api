from celery import Celery
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from mrsservice.blueprints.exceptions import error_handler
from mrsservice.blueprints.user import user
from mrsservice.blueprints.ticket import ticket

import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from mrsservice.extensions import (
    odoo, redis, babel, cache
)

_logger = logging.getLogger(__name__)

CELERY_TASK_LIST = [
    'mrsservice.blueprints.transaction.tasks',
    'mrsservice.blueprints.webhook.tasks',
    'mrsservice.blueprints.partner.tasks',

]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)
    middleware(app)
    app.register_blueprint(user)
    app.register_blueprint(error_handler)
    app.register_blueprint(ticket)
    extensions(app)
    setLogger(app)

    return app


def setLogger(app):
    logger = logging.getLogger('apis')
    file_handler = RotatingFileHandler('apis.log', backupCount=1)
    handler = logging.StreamHandler()
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s : %(message)s '
        '[in %(module)s: %(pathname)s:%(lineno)d]'
    ))
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(module)s: %(pathname)s:%(lineno)d]'
    ))
    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    odoo.init_app(app)
    redis.init_app(app)
    babel.init_app(app)
    cache.init_app(app)

    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None
