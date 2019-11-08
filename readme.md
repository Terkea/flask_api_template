# API template
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

- The `api_log` table stores all the requests which have been made.
To keep track of those changes simply call on the endpoint method
```
write_log(method, resource, request_args, token)
```
- Usually during the development process, even if I know it is not ideal I
 like to tweak the database schema. To keep track of all those changes
  `flask-migrate` comes in handy. Once you update the `models.py` file run
  from the root directory.
 ```shell script
python migrate.py db migrate
python migrate.py db upgrade
``` 


## Getting started
First of all we have to establish a connection with the database. To do so fill those fields which can be found inside `app/__init__.py`
```python
# DATABASE CREDENTIALS
ENGINE = 'mysql'
USERNAME = 'test'
PASSWORD = 'testtest'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'api'

```
Then create the tables. _Make sure that you run those command from the root folder_

~~~shell script
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
~~~

## Template for new endpoints
```python
@app.route('/api/endpoint', methods=['GET'])
def get_all_endpoints(current_user):
    pass



@app.route('/api/endpoint/<endpoint_id>', methods=['GET'])
def get_one_endpoint(current_user, endpoint_id):
    pass



@app.route('/api/endpoint', methods=['POST'])
def create_endpoint(current_user):
    pass



@app.route('/api/endpoint/<endpoint_id>', methods=['PUT'])
def update_endpoint(current_user, endpoint_id):
    pass



@app.route('/api/endpoint/<endpoint_id>', methods=['DELETE'])
def delete_endpoint(current_user, endpoint_id):
    pass
```

| RESOURCE  | GET  | POST | PUT | DELETE
| :-------- |-----:| ----:| ---:| -----:|
| SUCCESS       | 200 | 201 | 401 | 200
| UNAUTHORISED  | 401 | 401 | 401 | 401
| ERROR         | 404 | 404 | 404 | 404
| NOT FOUND     | 204 | 204 | 204 | 204

## REQUIREMENTS
- [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-Script](https://flask-script.readthedocs.io/en/latest/)
- [werkzeug](https://werkzeug.palletsprojects.com/en/0.15.x/utils/#module-werkzeug.security)
- [uuid](https://docs.python.org/3.6/library/uuid.html)
- [PyJWT](https://github.com/GehirnInc/python-jwt)
- [requests]()
