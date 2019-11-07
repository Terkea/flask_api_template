# restAPI template
## DESCRIPTION
- The `models` file can be found in the User class which serves as a 
basic template. It meets all the requirements essential to get started with.

- Each user has a `public_id` which is used as a `unique identifier` when querying
the database to prevent the case when people seek to find out how many users are 
stored in there and numerous other inconveniences.The values are generated
by `uuid.uuid4()`.

- `@token_required` makes sure that before querying the user exist and has a
valid token. Each token is `encoded` using the `config['SECRET_KEY']` and has
a lifespan of 365 days by default.

- Attach the following code on the top of the defined method to make 
the endpoint `admin-only`
```python3
if not current_user.admin:
    return jsonify({"message" : "Cannot perform that function!"}), 401
```

- The encryption for passwords is done by `werkzeug.security` module 
and the algorithm used is `sha256`


## Template for new endpoints
```python
@app.route('/api/endpoint', methods=['GET'])
@token_required
def get_all_endpoints(current_user):
    return jsonify({'endpoints' : output})



@app.route('/api/endpoint/<endpoint_id>', methods=['GET'])
@token_required
def get_one_endpoint(current_user, endpoint_id):
    return jsonify({'endpoints' : output})



@app.route('/api/endpoint', methods=['POST'])
@token_required
def create_endpoint(current_user):
    return jsonify({'message' : "endpoint created!"})



@app.route('/api/endpoint/<endpoint_id>', methods=['PUT'])
@token_required
def complete_endpoint(current_user, endpoint_id):
    return jsonify({'message' : 'endpoint item has been completed!'})



@app.route('/api/endpoint/<endpoint_id>', methods=['DELETE'])
def delete_endpoint(current_user, endpoint_id):
    return jsonify({'message' : 'endpoint item deleted!'})
```


## REQUIREMENTS
- [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [werkzeug](https://werkzeug.palletsprojects.com/en/0.15.x/utils/#module-werkzeug.security)
- [uuid](https://docs.python.org/3.6/library/uuid.html)
- [PyJWT](https://github.com/GehirnInc/python-jwt)
- [requests]()
