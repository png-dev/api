from flask import (
    Blueprint, request, make_response, json, jsonify, g
)
from mrsservice.extensions import (odoo)
from model import User
from validator import LoginInput
from mrsservice.blueprints.exceptions.exceptions import *
from datetime import datetime, timedelta
from flask import current_app
from mrsservice.extensions import redis
import jwt
from jwt import DecodeError, ExpiredSignature
from functools import wraps
import logging

logger = logging.getLogger('apis')

user = Blueprint('user', __name__, url_prefix='/api/v1/users')


def get_token_key(token):
    return "{}::{}".format(current_app.config['TOKEN_PREFIX'], token)


def create_token(user):
    payload = {
        'token': user['token'],
        'uid': user['uid'],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    redis.set(get_token_key(token), 'login:{}'.format(user['login']))
    redis.expire(get_token_key(token), 604800)
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization')
    if not redis.exists(get_token_key(token)):
        raise Exception('Token not found')
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            raise Unauthorized('Missing Authorization Header')
        try:
            payload = parse_token(request)
        except DecodeError as de:
            raise Unauthorized('Invalid Token {}'.format(de))
        except ExpiredSignature:
            raise Unauthorized('Expired Token')
        except Exception:
            raise Unauthorized('Token not found')

        g.token = payload['token']
        g.uid = payload['uid']
        return f(*args, **kwargs)

    return decorated_function


@user.route('/login', methods=['POST'])
def login():
    """
    :param:
        - email
        - password
    :return:
        - token
    """
    login_input = LoginInput(request)
    if not login_input.validate():
        raise InvalidUsage('Login data is invalid: {}'.format(login_input.errors))
    data = request.get_json(force=True, silent=True)
    try:
        res = User.login(data_input=data)
        jwt_token = create_token(user={'token': res['token'], 'uid': res['uid'], 'login': data['email']})
        response = make_response(
            jsonify({'token': jwt_token, 'message': 'login successful', 'email': data['email']})
        )
        response.status_code = 200
        return response

    except Exception as exc:
        raise Unauthorized('Username or Password is invalid {}'.format(exc))
