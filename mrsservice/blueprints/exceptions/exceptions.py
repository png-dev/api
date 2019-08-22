#! -*- coding: utf-8 -*-


class ServiceException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidUsage(ServiceException):
    status_code = 400


class Unauthorized(ServiceException):
    status_code = 401


class ApiServerError(ServiceException):
    status_code = 500


class AppMobileError(ServiceException):
    status_code = 426  # upgrade client software


# TODO Define more Exception to notify frontend
# - Backend Timeout
# - Backend Error
# - ....

# Các exception của backend đều inherit tư backendServerException

class BackendServerException(ServiceException):
    pass


class TimeoutBackendServerError(BackendServerException):
    status_code = 408


class ExecuteBackendServerError(BackendServerException):
    status_code = 520


class PartnerNotFound(ServiceException):
    status_code = 454
