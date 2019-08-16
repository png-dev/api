import flask
from flask import request, jsonify
import requests, json
import jwt
import os

app = flask.Flask(__name__)

# URL = os.environ.get('URL', 'https://dtw-management-core-1beed72f-odoo.dnpwater.net/')
URL = os.environ.get('URL', 'http://127.0.0.1:8069/')


@app.route('/api/v1/users/login', methods=['POST'])
def login():
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
    try:
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
        res = {'token': token.decode('unicode_escape')}
        return jsonify(res), 200
    except Exception as e:
        return '', 201


@app.route('/api/v1/tickets', methods=['GET'])
def getAll():
    URL_LIST_TICKETS = URL + "api/helpdesk.ticket/method/get_all_tickets?"

    token = request.headers.get("Authorization")
    payload_data = jwt.decode(token, 'SECRET_KEY', algorithms="HS256")
    token_odoo = payload_data['token']
    user_id = payload_data['uid']

    URL_LIST_TICKETS = URL_LIST_TICKETS + "token=" + token_odoo + "args={'user_id': " + user_id + "}"
    responseListCheck = requests.get(URL_LIST_TICKETS)
    jsonData = json.loads(responseListCheck.text)
    return jsonData
    # try:
    #     listCheckIn = jsonData['success']
    #     return jsonify(listCheckIn), 200
    # except Exception as e:
    #     return '', 201


@app.route('/api/v1/tickets/{id}', methods=['GET'])
def getDetailTickets():
    print ('')


@app.route('/api/v1/tickets/update/{id}', methods=['PUT'])
def update(id):
    try:
        URL_TICKETS = URL + 'api/helpdesk.ticket/update/' + str(id)
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
            'lat': lat,
            'lng': lng,
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
        headers['Content-Type'] = "application/json";
        response = requests.post(URL_CHECKIN, data=requestBody, headers=headers)
        return response.text
    except e:
        return '', 201


@app.route('/api/v1/tickets/problem/{id}', methods=['PUT'])
def problem(id):
    try:
        URL_TICKETS = URL + 'api/helpdesk.ticket/update/' + str(id)

        image_url = request.json['image_url']
        lat = request.json['lat']
        lng = request.json['lng']
        work_incident = request.json['work_incident']
        token = request.headers.get("Authorization")

        payload_data = jwt.decode(token, 'SECRET_KEY', algorithms="HS256")
        user_id = payload_data['uid']
        token_odoo = payload_data['token']

        params = {
            'image_url': image_url,
            'lat': lat,
            'lng': lng,
            'work_incident': work_incident,
        }
        requestBodyArray = {
            'token': token_odoo,
            'update_vals': params
        }
        requestBodyForm = {'params': requestBodyArray}
        requestBody = json.dumps(requestBodyForm)

        headers = {}
        headers['Content-Type'] = "application/json";
        response = requests.post(URL_CHECKIN, data=requestBody, headers=headers)
        return response.text
    except e:
        return '', 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
