#! -*- coding: utf-8 -*-

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

login_schema = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'required': [
        "email",
        "password",
    ],
    'properties': {
        'email': {
            'type': 'string',
        },
        'password': {
            'type': 'string',
        },
    }
}


class LoginInput(Inputs):
    json = [JsonSchema(schema=login_schema)]
