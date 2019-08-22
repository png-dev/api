#! -*- coding: utf-8 -*0

from flask import make_response
from flask import jsonify

from flask.blueprints import Blueprint
from exceptions import ServiceException
import logging

_logger = logging.getLogger(__name__)

error_handler = Blueprint('error_hander', __name__)


@error_handler.app_errorhandler(ServiceException)
def handle_serviceexception(e):
    res = make_response(jsonify(e.to_dict()))
    res.status_code = e.status_code
    _logger.debug("Error: {}".format(e))
    return res
