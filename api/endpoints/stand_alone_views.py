import datetime

import jwt
from flask import request, make_response, jsonify
from flask.views import View
from werkzeug.security import check_password_hash

from api import app
from api.models import User


class Login(View):
    def dispatch_request(self):
        # get the request authorization information
        auth = request.authorization

        # if there's no auth at all or username or password return
        if not auth or not auth.username or not auth.password:
            return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = User.query.filter_by(email=auth.username).first()
        if not user:
            return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            # generate token
            token = jwt.encode(
                # the token lasts 356 days, eventually can be changed later on
                {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


app.add_url_rule('/api/login/', view_func=Login.as_view('login'))
