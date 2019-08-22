from mrsservice.extensions import (odoo)
from flask import json
import logging

logger = logging.getLogger('apis')


class User():

    @classmethod
    def login(cls, data_input):
        login = data_input['email']
        password = data_input['password']
        res = odoo.authenticate(login, password)
        return res
