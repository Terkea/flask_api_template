from flask.views import MethodView

from api import app, db
from flask import request, jsonify
import uuid
from werkzeug.security import generate_password_hash
from api.models import User
import jwt
from functools import wraps


class UserEndpoint(MethodView):
    def token_required(self):
        """
        Decorator meant to check if the token exists or not
        If the token exists check if it is valid
        """
        @wraps(self)
        def decorated(*args, **kwargs):
            token = None

            if 'token' in request.headers:
                token = request.headers['token']

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                User.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            return self(*args, **kwargs)

        return decorated

    def get_user_by_token(self):
        """
        :param token: has to be a jwt token
        :return: the user based on the public_id supplied by the token
        """
        token = request.headers['token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(public_id=data['public_id']).first()
        return user


    @token_required
    def get(self, public_id):
        """
        :return:
        if current_user admin:
            if public_id None:
                all records
            else:
                specific record
        else:
            if public_id None:
                401
            else:
                if public_id represents the current user:
                    specific record
                else:
                    401
        :param public_id: user id
        """
        current_user = self.get_user_by_token()

        if current_user.admin:
            if public_id is None:
                users = User.query.all()
                output = []
                for user in users:
                    user_data = {'public_id': user.public_id, 'email': user.email, 'password': user.password,
                                 'admin': user.admin}
                    output.append(user_data)
                return jsonify({'users': output}), 200
            else:
                user = User.query.filter_by(public_id=public_id).first()
                if not user:
                    return jsonify({"message": "No user found!"}), 204

                user_data = {'public_id': user.public_id, 'email': user.email, 'password': user.password,
                             'admin': user.admin}

                return jsonify({"user": user_data}), 200
        else:
            if public_id is None:
                return jsonify({"message": "Cannot perform that function!"}), 401
            else:
                if current_user.public_id == public_id:
                    user = User.query.filter_by(public_id=public_id).first()
                    if not user:
                        return jsonify({"message": "No user found!"}), 204

                    user_data = {'public_id': user.public_id, 'email': user.email, 'password': user.password,
                                 'admin': user.admin}

                    return jsonify({"user": user_data}), 200
                else:
                    return jsonify({"message": "Cannot perform that function!"}), 401


    def post(self):
        """
        :rtype: response
        """
        try:
            data = request.get_json()
            hashed_password = generate_password_hash(data['password'], method='sha256')
            new_user = User(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password, admin=False)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': "New user created!"}), 201
        except:
            return jsonify({'message': "Error while creating new user!"}), 404

    @token_required
    def delete(self, public_id):
        """
        :rtype: response
        """
        current_user = self.get_user_by_token()
        if current_user.admin:
            user = User.query.filter_by(public_id=public_id).first()
            if not user:
                return jsonify({"message": "No user found!"}), 204

            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "The user has been deleted!"}), 201
        else:
            return jsonify({"message": "Cannot perform that function!"}), 401

    @token_required
    def put(self, public_id):
        """
        :param public_id: user public_id
        :return:
        if current_user admin:
            update the user with that public_id
        else:
            if the current_user is the user that public_id:
                update
            else: 401

        """
        current_user = self.get_user_by_token()

        update_user = User.query.filter_by(public_id=public_id).first()
        if not update_user:
            return jsonify({"message": "No user found!"}), 204

        if current_user.admin:
            update_data = request.get_json()
            try:
                update_user.email = update_data['email']
            except:
                pass

            try:
                update_user.password = generate_password_hash(update_data['password'], method='sha256')
            except:
                pass

            try:
                update_user.admin = update_data['admin']
            except:
                pass

            try:
                db.session.commit()
                return jsonify({"message": "The user has been updated!"}), 201
            except:
                return jsonify({"message": "error while updating"}), 404

        else:
            if current_user.public_id == public_id:
                update_data = request.get_json()
                try:
                    update_user.email = update_data['email']
                except:
                    pass

                try:
                    update_user.password = generate_password_hash(update_data['password'], method='sha256')
                except:
                    pass

                try:
                    db.session.commit()
                    return jsonify({"message": "The user has been updated!"}), 201
                except:
                    return jsonify({"message": "error while updating"}), 404
            else:
                return jsonify({"message": "Cannot perform that function!"}), 401


user_view = UserEndpoint.as_view('user_api')
app.add_url_rule('/api/users/', defaults={'public_id': None},
                 view_func=user_view, methods=['GET', ])
app.add_url_rule('/api/users/', view_func=user_view, methods=['POST', ])
app.add_url_rule('/api/users/<string:public_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])