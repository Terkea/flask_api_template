# API
This is meant to be a template for starting new API's

## REQUIREMENTS
- [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [werkzeug.security](https://werkzeug.palletsprojects.com/en/0.15.x/utils/#module-werkzeug.security)
- 

## USAGE
### GET
###### RESPONSE 
- `200 OK` on success
- `404 Not Found` if object doesn't exist
~~~
/endpoint/get/{id}
~~~
Returns a specific object by id


###### RESPONSE 
- `200 OK` on success
~~~
/endpoint/get/
~~~
Returns all objects

###  POST
~~~
/endpoint/post/**kwargs
~~~
- `201 Created` on success

###  DELETE
~~~
/endpoint/delete/{id}
~~~
- `202 No Content` on success
- `404 Not found` if there's no object with that id
