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

- The encryption for passwords is done by `werkzeug.security` module 
and the algorithm used is `sha256`

- Usually during the development process, even if I know it is not ideal I
 like to tweak the database schema. To keep track of all those changes
  `flask-migrate` comes in handy. Once you update the `models.py` file run
  from the root directory.
 ```
python migrate.py db migrate
python migrate.py db upgrade
``` 


## Getting started
First of all we have to establish a connection with the database. To do so fill those fields which can be found inside `app/__init__.py`
```python
# DATABASE CREDENTIALS
ENGINE = 'mysql'
USERNAME = 'name'
PASSWORD = 'password'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'api'

```
Then create the tables. _Make sure that you run those command from the root folder_

~~~
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
~~~

## Endpoints
- Each one has a [MethodView](https://flask.palletsprojects.com/en/1.1.x/views/) class file with the name of the model in `/api/endpoints`
- Stand-alone routes are written in `endpoints/stand_alone_views`
- After creating a new endpoint don't forget to import it in `__init__.py`


### Template for new endpoints
```python
class Endpoint(MethodView):

    def get(self, endpoint_id):
        if endpoint_id is None:
            # return a list of endpoints
            pass
        else:
            # expose a single endpoint
            pass

    def post(self):
        # create a new user
        pass

    def delete(self, endpoint_id):
        # delete a single endpoint
        pass

    def put(self, endpoint_id):
        # update a single endpoint
        pass
```

### Easy to customize content-delivery
For example the endpoint `user GET` delivers its content as following
```
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
```
### Response for user Endpoint

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
