from mrsservice.extensions import (
    odoo
)
from flask import json, request, g
import logging

logger = logging.getLogger('apis')


class Ticket():
    _model_name = 'helpdesk.ticket'

    @classmethod
    def search_ids(cls, domain, offset, limit):
        return odoo.search_ids(model=cls._model_name,
                               domain=domain, offset=offset, order='name desc', limit=limit)

    @classmethod
    def execute_method(cls, ticket_ids, method_name, kwargs=None):
        if len(ticket_ids) == 0:
            return []
        res = odoo.call_method(model=cls._model_name, record_ids=ticket_ids, method=method_name, kwargs=kwargs)
        return res

    @classmethod
    def create_ticket(cls, vals):
        res = odoo.create_method(model=cls._model_name, vals=vals)
        ticket_id = res['id']
        return {'message': 'success', 'id': ticket_id}

    @classmethod
    def report_ticket(cls, record_id, vals):
        logger.info('debug {}'.format(vals))
        lat = vals[u'lat']
        lng = vals[u'lng']
        image_urls = vals[u'image_url']
        work_incident = vals[u'work_incident']

        vals_update = {
            u'work_incident': work_incident,
            u'kanban_state': u'done',
        }
        res = odoo.update_method(model=cls._model_name, vals=vals_update, record_id=record_id, token=g.token)

        for x in image_urls:
            val_create = {
                u'lat': lat,
                u'lng': lng,
                u'image_url': str(x),
                u'id_ticket': int(record_id),
                u'gps_action': 'work_incident'
            }
            resCreate = odoo.create_method(model='helpdesk.ticket.coordinates', vals=val_create)
            ticket_id = resCreate['id']
        return {'message': 'success'}

    @classmethod
    def update_ticket(cls, record_id, vals):
        logger.info('debug {}'.format(vals))
        lat = vals[u'lat']
        lng = vals[u'lng']
        image_urls = vals[u'image_url']
        results = vals[u'results']

        vals_update = {
            u'results': results,
            u'kanban_state': u'done',
        }
        res = odoo.update_method(model=cls._model_name, vals=vals_update, record_id=record_id, token=g.token)

        for x in image_urls:
            val_create = {
                u'lat': lat,
                u'lng': lng,
                u'image_url': str(x),
                u'id_ticket': int(record_id),
                u'gps_action': 'results'
            }
            resCreate = odoo.create_method(model='helpdesk.ticket.coordinates', vals=val_create)
            ticket_id = resCreate['id']
        return {'message': 'success'}

    @classmethod
    def get_tickets(cls, filter):
        if filter.get('ticket_id'):
            ticket_ids = [filter.get('ticket_id')]
            res = cls.execute_method(ticket_ids=ticket_ids, method_name='get_detail_ticket')
        else:
            domain = []
            domain.append(('user_id', '=', g.uid))
            offset = filter.get('offset')
            limit = filter.get('limit')
            ticket_ids = cls.search_ids(domain=domain, offset=offset, limit=limit)
            res = cls.execute_method(ticket_ids=ticket_ids, method_name='get_all_tickets')
        return res
