from api import app, api
from flask_restful import Resource
from flask import jsonify

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')