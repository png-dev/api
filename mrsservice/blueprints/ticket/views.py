from flask import (
    Blueprint, request, make_response, json, g
)

from mrsservice.extensions import (
    odoo, cache
)
from mrsservice.blueprints.user.views import login_required
from mrsservice.blueprints.exceptions.exceptions import *
from validators import TicketUpdate, TicketProblem
from .model import Ticket
import logging

logger = logging.getLogger('apis')

ticket = Blueprint('ticket', __name__, url_prefix='/api/v1/tickets')


def make_key():
    return str(g.token) + str(request.full_path)


@ticket.route('/', methods=['GET'], defaults={'ticket_id': 0})
@ticket.route('/<int:ticket_id>', methods=['GET'])
@login_required
def get_tickets(ticket_id=0):
    try:
        filter = {
            'ticket_id': ticket_id,
            'offset': int(request.args.get('offset', 0)),
            'limit': int(request.args.get('limit', False)),
        }
    except Exception as ex:
        raise InvalidUsage('Parameter is invalid: {}'.format(ex))

    data = Ticket.get_tickets(filter=filter)
    response = make_response(json.dumps(data))
    response.status_code = 200
    return response


@ticket.route('/<int:ticket_id>/actions/SetToDone', methods=['PUT'])
@login_required
def update_ticket(ticket_id=0):
    ticket_input = TicketUpdate(request)
    if not ticket_input.validate():
        raise InvalidUsage('Data is invalid: {}'.format(ticket_input.errors))

    jdata = request.get_json(force=True, silent=True)

    res = Ticket.update_ticket(record_id=ticket_id, vals=jdata)
    response = make_response(json.dumps(res))
    response.status_code = 200
    return response


@ticket.route('/<int:ticket_id>/actions/ReportProblem', methods=['PUT'])
@login_required
def problem_ticket(ticket_id=0):
    ticket_input = TicketProblem(request)
    if not ticket_input.validate():
        raise InvalidUsage('Data is invalid: {}'.format(ticket_input.errors))

    jdata = request.get_json(force=True, silent=True)
    res = Ticket.report_ticket(ticket_id, vals=jdata)
    response = make_response(json.dumps(res))
    response.status_code = 200
    return response
