from api import app, db
from flask import Flask, request, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User

# USER ENDPOINTS
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
def get_specific_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message" : "No user found!"})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({"user" : user_data})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : "New user created!"}), 200

@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message" : "No user found!"})

    user.admin = True
    db.session.commit()

    return jsonify({"message" : "The user has been promoted!"})

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message" : "No user found!"})

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message" : "The user has been deleted!"})