from werkzeug.security import check_password_hash
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import datetime
import jwt
import json
# from bson import json_util
from functools import wraps
from db import get_user, get_users, post_user, update_user, get_rwp_designs, get_all_designs, get_isb_designs, get_user_designs, user_dislikes_design, user_likes_design, get_search_items, get_most_liked_designs_cat_wise, get_most_liked_designs_cat_city_wise, get_category_items, ratings_table_insertion, predictions

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
                    # 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)
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


class AllDesigns(Resource):
    @token_required
    def get(self, cur_user):
        try:
            designs = get_all_designs()
            return {'Designs' : designs}, 200
        except Exception as e:
            return {'msg': 'Design not found'}, 500

class RwpDesigns(Resource):
    @token_required
    def get(self, cur_user):
        try:
            token = request.headers['x-access-token']
            user = jwt.decode(token, 'mysecretkey')
            designs = get_rwp_designs(user['username'])
            return {'Designs' : designs}, 200
        except Exception as e:
            return {'msg': 'Design not found'}, 500

class IsbDesigns(Resource):
    @token_required
    def get(self, cur_user):
        try:
            token = request.headers['x-access-token']
            user = jwt.decode(token, 'mysecretkey')
            designs = get_isb_designs(user['username'])
            return {'Designs' : designs}, 200
        except Exception as e:
            return {'msg': 'Design not found'}, 500

class GetUserLikes(Resource):
    @token_required
    def get(self, cur_user):
        try:
            token = request.headers['x-access-token']
            user = jwt.decode(token, 'mysecretkey')
            designs = get_user_designs(user['username'] )
            return {'Designs' : designs}, 200
        except Exception as e:
            return {'msg': 'Design not found'}, 500

    @token_required
    def post(self, cur_user):
        try:
            data = request.get_json(force=True)
            print(data['image'])
            token = request.headers['x-access-token']
            user = jwt.decode(token, 'mysecretkey')
            designs = user_likes_design(data['image'],user['username'])
            return {'Designs' : designs}, 200
        except Exception as e:
            return {'msg': 'Design not found'}, 500

    @token_required
    def put(self, cur_user):
        try:
            data = request.get_json(force=True)
            token = request.headers['x-access-token']
            user = jwt.decode(token, 'mysecretkey')
            designs = user_dislikes_design(data['image'],user['username'])
            return {'Designs' : designs}, 200
        except Exception as e:
            return {'msg': 'Design not found'}, 500


class GetUsers(Resource):
    def get(self):
        try:
            users = get_users()
            return {'Users' : users}, 200
        except Exception as e:
            return {'msg': 'User not found'}, 500

class GetUser(Resource):
    @token_required
    def get(self, cur_user):
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
            return {'msg': 'Error Updating User'}, 500

class GetDesignList(Resource):
    @token_required
    def get(self, current_user):
        try:
            resp = get_search_items()
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error Performing Operation'}, 500

class GetCatList(Resource):
    @token_required
    def get(self, current_user):
        try:
            resp = get_category_items()
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error Performing Operation'}, 500


class GetCatWiseDesign(Resource):
    @token_required
    def get(self, current_user):
        data = request.get_json(force=True)
        try:
            cat = data['cat']
            resp = get_most_liked_designs_cat_wise(cat)
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error Performing Operation'}, 500
   

class GetCatCityWiseDesign(Resource):
    @token_required
    def get(self, current_user):
        data = request.get_json(force=True)
        try:
            cat = data['cat']
            city = data['city']
            resp = get_most_liked_designs_cat_city_wise(cat, city)
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error Performing Operation'}, 500
    
class RateDesigns(Resource):
    @token_required
    def post(self, current_user):
        data = request.get_json(force=True)
        try:
            token = request.headers['x-access-token']
            tokenData = jwt.decode(token, 'mysecretkey')
            user = tokenData['username']
            image = data['image']
            rating = data['rating']
            resp = ratings_table_insertion(user, image, rating)
            return {'msg': resp}, 200
        except Exception:
            return {'msg': 'Error Performing Operation'}, 500
    
class GetPredictions(Resource):
    @token_required
    def get(self, current_user):
        try:
            token = request.headers['x-access-token']
            data = jwt.decode(token, 'mysecretkey')
            user = data['username']
            resp = predictions(user)
            return {'Designs': resp}, 200
        except Exception:
            return {'msg': 'Error Performing Operation'}, 500
    

api.add_resource(Login, '/api/login')
api.add_resource(GetUsers, '/api/users/')
api.add_resource(GetUser, '/api/user/')
api.add_resource(UserActions, '/api/useractions')
# api.add_resource(AllDesigns, '/api/designs')
api.add_resource(RwpDesigns, '/api/designs/rawalpindi')
api.add_resource(IsbDesigns, '/api/designs/islamabad')
api.add_resource(GetUserLikes, '/api/designs/userdesign')
api.add_resource(GetDesignList, '/api/searchlist')
api.add_resource(GetCatList, '/api/catlist')
api.add_resource(GetCatWiseDesign, '/api/designs/cat')
api.add_resource(GetCatCityWiseDesign, '/api/designs/cat/city')
api.add_resource(RateDesigns, '/api/designs/rate')
api.add_resource(GetPredictions, '/api/designs/preds')

if __name__=='__main__':
    app.run(debug=True)