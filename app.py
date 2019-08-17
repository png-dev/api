import flask
from flask import request, jsonify
import requests, json
import jwt
import os
import logging

__logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

# URL = os.environ.get('URL', 'https://dtw-management-core-1beed72f-odoo.dnpwater.net/')
URL = os.environ.get('URL', 'http://192.168.43.21:8069/')


@app.route('/api/v1/users/login', methods=['POST'])
def login():
    try:
        login = request.json['login']
        password = request.json['password']
        URL_LOGIN = URL + 'api/user/get_token'
        params = {
            'login': login,
            'password': password
        }
        if params is not None:
            URL_LOGIN += '?'
        for key in params:
            URL_LOGIN += key + '=' + params[key] + '&'
        response = requests.get(URL_LOGIN)
        data = json.loads(response.text)
        result = data['success']
        payload = {
            'token': result['token'],
            'uid': result['uid']
        }
        token = jwt.encode(
            payload,
            'SECRET_KEY',
            algorithm='HS256'
        );
        res = {'token': token.decode('unicode_escape'), 'name': result['name']}
        return jsonify(res), 200
    except Exception as e:
        return '', 201


@app.route('/api/v1/tickets', methods=['GET'])
def getAll():
    try:
        URL_LIST_TICKETS = URL + "api/helpdesk.ticket/method/get_all_tickets?"
        URL_LIST_ID = URL + "api/helpdesk.ticket/search?"
        token = request.headers.get("Authorization")
        payload_data = jwt.decode(token, 'SECRET_KEY', algorithms="HS256")
        token_odoo = payload_data['token']
        user_id = payload_data['uid']

        URL_LIST_ID = URL_LIST_ID + "token=" + token_odoo + "&domain=[('user_id', '=', " + str(user_id) + ")]"
        responseListId = requests.get(URL_LIST_ID)
        jsonids = json.loads(responseListId.text)
        listIds = '[ '
        for id in jsonids:
            strid = id['id']
            listIds = listIds + str(strid) + ', '
        listIds = listIds + ' ]'
        URL_LIST_TICKETS = URL_LIST_TICKETS + "token=" + token_odoo + "&ids=" + listIds
        responseListTickets = requests.get(URL_LIST_TICKETS)
        jsonData = json.loads(responseListTickets.text)
        listTickets = jsonData['success']
        return jsonify(listTickets), 200
    except Exception as e:
        return '', 201


@app.route('/api/v1/tickets/<int:id>', methods=['GET'])
def getDetailTickets(id=0):
    try:
        URL_TICKET = URL + "api/helpdesk.ticket/method/get_detail_ticket?"
        token = request.headers.get("Authorization")
        payload_data = jwt.decode(token, 'SECRET_KEY', algorithms="HS256")
        token_odoo = payload_data['token']
        user_id = payload_data['uid']
        id_ticket = '[' + str(id) + ',]'
        URL_TICKET = URL_TICKET + "token=" + token_odoo + "&ids=" + id_ticket
        responseTicket = requests.get(URL_TICKET)
        jsonData = json.loads(responseTicket.text)
        listTicket = jsonData['success']
        return jsonify(listTicket), 200
    except Exception as e:
        return '', 201


@app.route('/api/v1/tickets/update/<int:id>', methods=['PUT'])
def update(id=0):
    try:
        URL_TICKET = URL + 'api/helpdesk.ticket/update/' + str(id)
        image_url = request.json['image_url']
        lat = request.json['lat']
        lng = request.json['lng']
        results = request.json['results']
        token = request.headers.get("Authorization")

        payload_data = jwt.decode(token, 'SECRET_KEY', algorithms="HS256")
        user_id = payload_data['uid']
        token_odoo = payload_data['token']

        params = {
            'image_url': image_url,
            'lat': float(lat),
            'lng': float(lng),
            'kanban_state': 'done',
            'results': results,
        }
        requestBodyArray = {
            'token': token_odoo,
            'update_vals': params
        }
        requestBodyForm = {'params': requestBodyArray}
        requestBody = json.dumps(requestBodyForm)

        headers = {}
        headers['Content-Type'] = "application/json"
        response = requests.post(URL_TICKET, data=requestBody, headers=headers)
        jsonData = json.loads(response.text)
        id = jsonData['id']
        if id:
            return '{"result": "success"}'
        else:
            return '{"result": "failed"}'
    except:
        return '', 201


@app.route('/api/v1/tickets/problem/<int:id>', methods=['PUT'])
def problem(id):
    try:
        URL_TICKET = URL + 'api/helpdesk.ticket/update/' + str(id)
        image_url = request.json['image_url']
        lat = request.json['lat']
        lng = request.json['lng']
        work_incident = request.json['work_incident']
        token = request.headers.get("Authorization")

        payload_data = jwt.decode(token, 'SECRET_KEY', algorithms="HS256")
        token_odoo = payload_data['token']

        params = {
            'image_url': image_url,
            'lat': float(lat),
            'lng': float(lng),
            'work_incident': work_incident,
        }
        requestBodyArray = {
            'token': token_odoo,
            'update_vals': params
        }
        requestBodyForm = {'params': requestBodyArray}
        requestBody = json.dumps(requestBodyForm)

        headers = {}
        headers['Content-Type'] = "application/json"
        response = requests.post(URL_TICKET, data=requestBody, headers=headers)
        jsonData = json.loads(response.text)
        id = jsonData['id']
        if id:
            return '{"result": "success"}'
        else:
            return '{"result": "failed"}'
    except:
        return '', 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
