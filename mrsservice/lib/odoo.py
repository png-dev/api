#! -*- coding: utf-8 -*-
import logging
import requests
import json
from mrsservice.blueprints.exceptions.exceptions import TimeoutBackendServerError, ExecuteBackendServerError, \
    InvalidUsage, Unauthorized
from flask import g
from flask import request

TIMEOUT = 3600
logger = logging.getLogger('apis')
import ast


# TODO: Try-catch và trả về Exception detail hơn khi connect với
# Các Exception được định nghĩa chi tiết ở blueprint Exception
# Các lỗi cơ bản: ko kết nối được backend, kết nối nhưng ko execute được ...
# Vì các hàm giống nhau nên có thể viết decorator để chạy .

class RequestOdoo():

    def get(self, url):
        try:
            res = requests.get(url=url, timeout=TIMEOUT).text
        except requests.exceptions.Timeout:
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, "Timeout get data")
            raise TimeoutBackendServerError('Timeout get data ')
        except requests.exceptions.RequestException as ex:
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, 'Error while get data   {}'.format(ex))
            raise ExecuteBackendServerError('Error while get data   {}'.format(ex))
        if 'error' in json.loads(res):
            res_data = json.loads(res)['error'].encode('utf-8')
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, res_data)
            if 'Invalid User Token' in res_data:
                raise Unauthorized("Invalid User Token")
            raise ExecuteBackendServerError('Error while get data   {}'.format(res_data))
        if 'success' in json.loads(res):
            res_data = json.loads(res)['success']
            return res_data
        return json.load(res)

    def post(self, url, data):
        try:
            headers = {'Content-Type': 'application/json'}
            res = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=TIMEOUT).text
            logger.info("debug {}".format(res))
        except requests.exceptions.Timeout:
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, 'Timeout execute ')
            raise TimeoutBackendServerError('Timeout execute ')
        except requests.exceptions.RequestException as ex:
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, 'Error while execute method {}'.format(ex))
            raise ExecuteBackendServerError('Error while execute method {}'.format(ex))
        if 'error' in json.loads(json.loads(res)['result']):
            res_data = json.loads(json.loads(res)['result'])['error'].encode('utf-8')
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, res_data)
            if 'Invalid User Token' in res_data:
                raise Unauthorized("Invalid User Token")
            raise ExecuteBackendServerError('Error while get data   {}'.format(res_data))
        if 'success' in json.loads(json.loads(res)['result']):
            res_data = json.loads(json.loads(res)['result'])['success']
            return res_data
        return json.loads(res)


class Odoo(RequestOdoo):
    def __init__(self, app=None, config=None):
        self.config = config
        self.request_odoo = RequestOdoo()
        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        if not (config is None or isinstance(config, dict)):
            raise ValueError("'config' must be an instance of dict or None")

        base_config = app.config.copy()
        if self.config:
            base_config.update(self.config)
        if config:
            base_config.update(config)
        self.config = base_config
        logger.info("debug config {}".format(self.config))

    def search_method(self, model, token=None, record_id=None, fields=None, domain=[], offset=None, limit=None,
                      order=None):
        if not token:
            token = g.token
        if record_id:
            url = '{0}/api/{1}/search/{2}?token={3}&fields={4}'.format(self.config['ODOO_URL'], model, record_id, token,
                                                                       fields)
        else:
            if order:
                url = '{0}/api/{1}/search?token={2}&fields={3}&domain={4}&offset={5}&limit={6}&order={7}'.format(
                    self.config['ODOO_URL'], model, token, fields, domain, offset, limit, order)
            else:
                url = '{0}/api/{1}/search?token={2}&fields={3}&domain={4}&offset={5}&limit={6}'.format(
                    self.config['ODOO_URL'], model, token, fields, domain, offset, limit)
        try:
            res = requests.get(url=url, timeout=TIMEOUT).text
        except requests.exceptions.Timeout:
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, 'Timeout get data ')
            raise TimeoutBackendServerError('Timeout get data ')
        except requests.exceptions.RequestException as ex:
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, 'Error while get data   {}'.format(ex))
            raise ExecuteBackendServerError('Error while get data   {}'.format(ex))
        if 'error' in json.loads(res):
            res_data = json.loads(res)['error'].encode('utf-8')
            from mrsservice.blueprints.webhook.tasks import notify
            notify(request, res_data)
            if 'Invalid User Token' in res_data:
                raise Unauthorized("Invalid User Token")
            raise ExecuteBackendServerError('Error while get data   {}'.format(res_data))
        return json.loads(res)

    def search_ids(self, model, token=None, domain=[], offset=None, limit=None, order=None):
        if not token:
            token = g.token
        if order:
            url = '{}/api/{}/search_ids?token={}&domain={}&offset={}&order={}'.format(
                self.config['ODOO_URL'], model, token, domain, offset, order)
            if limit:
                url = '{}/api/{}/search_ids?token={}&domain={}&offset={}&limit={}&order={}'.format(
                    self.config['ODOO_URL'], model, token, domain, offset, limit, order)
        else:
            url = '{}/api/{}/search_ids?token={}&domain={}&offset={}'.format(
                self.config['ODOO_URL'], model, token, domain, offset)
            if limit:
                url = '{}/api/{}/search_ids?token={}&domain={}&offset={}&limit={}'.format(
                    self.config['ODOO_URL'], model, token, domain, offset, limit)
        res = self.request_odoo.get(url)
        return res

    def create_method(self, model, vals):
        token = g.token
        data = {'params': {'create_vals': vals, 'token': token}}
        url = '{0}/api/{1}/create'.format(self.config['ODOO_URL'], model)
        res = self.request_odoo.post(url=url, data=data)
        return res

    def update_method(self, model, record_id, token, vals):
        if not token:
            token = g.token
        data = {'params': {'update_vals': vals, 'token': token}}
        url = '{0}/api/{1}/update/{2}'.format(self.config['ODOO_URL'], model, record_id)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=TIMEOUT).text
        logger.info("debug {}".format(res))
        # res = self.request_odoo.post(url=url, data=data)
        return res

    def delete_method(self, model, record_id, token):
        url = '{0}/api/{1}/unlink/{1}?token={2}'.format(self.config['ODOO_URL'], model, record_id, token)
        res = self.request_odoo.post(url=url, data={})
        return res

    def call_method(self, model, record_ids, method, token=None, fields=None, kwargs=None):
        if not token:
            token = g.token
        if kwargs:
            url = '{}/api/{}/method/{}?token={}&kwargs={}&ids={}'.format(self.config['ODOO_URL'], model, method, token,
                                                                         kwargs, record_ids)
        else:
            url = '{}/api/{}/method/{}?token={}&ids={}'.format(self.config['ODOO_URL'], model, method, token,
                                                               record_ids)

        if len(record_ids) == 1:
            if kwargs:
                url = '{0}/api/{1}/{2}/method/{3}?token={4}&kwargs={5}'.format(self.config['ODOO_URL'], model,
                                                                               record_ids[0],
                                                                               method, token, kwargs)
            else:
                url = '{0}/api/{1}/{2}/method/{3}?token={4}'.format(self.config['ODOO_URL'], model, record_ids[0],
                                                                    method,
                                                                    token)
        res = self.request_odoo.get(url=url)
        return res

    def call_method_post(self, model, record_id, method, token=None, fields=None, kwargs=None):
        if not token:
            token = g.token
        data = {'params': {'kwargs': kwargs, 'token': token}}
        url = '{0}/api/{1}/{2}/method/{3}'.format(self.config['ODOO_URL'], model, record_id,
                                                  method)
        res = self.request_odoo.post(url=url, data=data)
        return res

    def authenticate(self, login, password):
        url = "{0}/api/user/get_token?login={1}&password={2}".format(self.config['ODOO_URL'], login, password)
        res = self.request_odoo.get(url=url)
        return res

    def reset_password(self, login, password):
        res = requests.get(
            '{0}/api/user/reset_password?login={1}&password={2}'.format(self.config['ODOO_URL'], login, password),
            timeout=TIMEOUT)
        return res
