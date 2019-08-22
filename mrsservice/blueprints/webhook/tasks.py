#! -*- coding: utf-8 -*-

import logging
from mrsservice.app import create_celery_app
from slack import notify_message

_logger = logging.getLogger(__name__)

celery = create_celery_app()


@celery.task()
def notify_to_slack(message):
    try:
        notify_message(message)
    except Exception as e:
        _logger.info('Error notify message to slack  : {}'.format(e))


def notify(request, message):
    message_to_notify = error_message(request, message)
    notify_to_slack.delay(message_to_notify)


def error_message(request, message):
    data = {
        'body': request.get_json(force=True, silent=True),
        'api': request.url,
        'method': request.method,
        'headers': request.headers

    }
    return "api error: info " + str(data) + " message: " + str(message)
