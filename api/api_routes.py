from api import app, db
from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User
import jwt
import datetime
from functools import wraps
from sqlalchemy import or_


# ???
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/login')
def api_login():
    # get the request authorization information
    auth = request.authorization

    # if there's no auth at all or username or password return
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        # generate token
        token = jwt.encode(
            # the token lasts 30 minutes, eventually can be changed later on
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=356)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# USER ENDPOINTS
@app.route('/api/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    # if not admin cannot use the route
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/api/user', methods=['POST'])
@token_required
def create_user(current_user):
    # if not admin cannot use the route
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': "New user created!"}), 201


@app.route('/api/user/<public_id>', methods=['GET'])
@token_required
def get_specific_user(current_user, public_id):
    # if not admin cannot use the route
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "No user found!"}), 202

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({"user": user_data})


@app.route('/api/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    # if not admin cannot use the route
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "No user found!"}), 202

    user.admin = True
    db.session.commit()

    return jsonify({"message": "The user has been promoted!"}), 201


@app.route('/api/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    # if not admin cannot use the route
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "No user found!"})

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "The user has been deleted!"})

@app.route('/api/search_user', methods=['GET'])
@token_required
def search_with_multiple_filters(current_user):
    # if not admin cannot use the route
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"}), 401

    args = request.get_json()
    search_filters = {'public_id': args.get("public_id"), 'name': args.get("name"), 'password': args.get("password"),
               'admin': args.get("admin")}

    users = User.query.filter(or_(User.public_id == search_filters['public_id'], User.password ==
                                  search_filters['password'], User.name == search_filters['name'],
                                  User.admin == search_filters['admin']))

    output = []
    for user in users:
        user_data = {'public_id': user.public_id, 'name': user.name, 'password': user.password, 'admin': user.admin}
        output.append(user_data)

    return jsonify({'users': output})

# USER ENDPOINTS END
