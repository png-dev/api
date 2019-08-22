#! -*- coding: utf-8 -*-

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

ticket_update_schema = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'required': [
        "image_url",
        "results"
    ],
    'properties': {
        'lng': {
            'type': 'number',
        },
        'lat': {
            'type': 'number',
        },
        'results': {
            'type': 'string',
        },
        'image_url': {
            'type': 'array',
        },

    }
}


class TicketUpdate(Inputs):
    json = [JsonSchema(schema=ticket_update_schema)]


ticket_problem_schema = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'required': [
        "image_url",
        "work_incident"
    ],
    'properties': {
        'lng': {
            'type': 'number',
        },
        'lat': {
            'type': 'number',
        },
        'work_incident': {
            'type': 'string',
        },
        'image_url': {
            'type': 'array',
        },

    }
}


class TicketProblem(Inputs):
    json = [JsonSchema(schema=ticket_problem_schema)]
