from werkzeug.security import check_password_hash
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import datetime
import jwt
import json
from bson import json_util
from functools import wraps
from db import get_user, get_users, post_user, update_user

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "mysecretkey"
CORS(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'msg': 'Token is missing'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = get_user(data['username'])
        except Exception as e:
            print(e)
            return {'msg': 'Token is invalid'}, 401

        return f(current_user, *args, **kwargs)
    return decorated

class Login(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            username = data['username']
            password = data['password']
            if not username or not password:
                return make_response(
                    'User or password is empty',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login required!"'})

            user = get_user(username)

            if not user:
                return make_response(
                    'Username or password is invalid',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login required!"'})

            if password != user['Password']:
                return make_response(
                    'Username or password is invalid',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login required!"'})

            token = jwt.encode({
                    'username': user['Username'],
                    'fullName': user['FirstName'] + " " + user['LastName'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)
                },
                    app.config['SECRET_KEY']
                )
            return {'token': token.decode('UTF-8')}, 200
        except Exception as e:
            print(e)
            return make_response(
                    'Could not authenticate',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login required!"'})

class GetUsers(Resource):
    def get(self):
        try:
            users = get_users()
            return {'Users' : users}, 200
        except Exception as e:
            return {'msg': 'User not found'}, 500


class GetUser(Resource):
    @token_required
    def get(self):
        try:
            token = request.headers['x-access-token']
            user = jwt.decode(token, 'mysecretkey')
            user = get_user(user['username'])
            return {'user' : user}, 200
        except Exception as e:
            return {'msg': 'User not found'}, 500

class UserActions(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            username = data['username']
            password = data['password']
            firstname = data['firstname']
            lastname = data['lastname']
            city = data['city']
            email = data['email']
            date = data['date']
            resp = post_user(username, firstname, lastname, city, email, password, date)
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error creating user'}, 500
    @token_required
    def put(self, current_user):
        data = request.get_json(force=True)
        try:
            username = data['username']
            password = data['password']
            firstname = data['firstname']
            lastname = data['lastname']
            city = data['city']
            email = data['email']
            resp = update_user(username, firstname, lastname, city, email, password)
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error updating user'}, 500

api.add_resource(Login, '/api/login')
api.add_resource(GetUsers, '/api/users/')
api.add_resource(GetUser, '/api/user/')
api.add_resource(UserActions, '/api/useractions')

if __name__=='__main__':
    app.run(debug=True)