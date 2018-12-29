import re
from flask import Flask, request, jsonify, make_response , Blueprint
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt)
from ..models import users
auth = Blueprint('auth', __name__, url_prefix='/api/v1')

BLACKLIST = set()
User = users.Users()

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    username = data.get('username').strip()
    name = data.get('name')
    email = data.get('email').strip()
    password = data.get('password').strip()
    confirm_password = data.get('confirm_password').strip()

    userinfo = [username, name,password, confirm_password, email]

    for info in userinfo:
        if info is None or not info :
            return jsonify({"message": "Make sure all field are filled out"}), 206

    if len(password) < 4:
        return jsonify({"message": "The password is too short,minimum length is 4"}), 400
    if confirm_password != password:
        return jsonify({"message": "The passwords you entered don't match"}), 400
    match = re.match(
        r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return jsonify({"message": "Enter a valid email address"}), 403
    response = jsonify(User.put(name, username, email, password))
    response.status_code = 201
    return response
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "fields cannot be emptyy"}),400
    username  = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Username or password is missing"}),206
    validated = User.password_validation(username,password)
    user = User.get_single_user(username)
    if validated == "True":
        acces_token = create_access_token(idenity=user)
        return jsonify(dict(token=acces_token, message="Login seccesfull")), 200
    response = jsonify(validated)
    response.status_code  = 401
    return response


@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():

    json_token_identifier = get_raw_jwt()['jti']
    BLACKLIST.add(json_token_identifier)
    return jsonify({"message": "Successfully logged out"}), 200


@auth.route('/users', methods=['GET'])
def get_all_users():
    response = make_response(jsonify(User.get_all_users()))
    response.status_code = 200
    return response


@auth.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    response = make_response(
        jsonify(User.get_single_user(username)))
    response.status_code = 200
    return response
