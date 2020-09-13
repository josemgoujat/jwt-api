# jwt-api
Minimal JWT authentication in Django

## Local setup
```
docker-compose build
docker-compose up --detach
docker exec -it jwt-api_web_1 python manage.py migrate
```

## Run tests
```
docker exec -it jwt-api_web_1 python manage.py test
```

## Usage
### 1. Create a User
Using Django Rest Framework browsable API, go to http://localhost:8000/auth/signup and post some credentials in the following format:
```
{"username":"myusername","password":"mypassword"}
```

### 2. Login and obtain JWT token
Go to http://localhost:8000/auth/login and post the same previous credentials to obtain the JWT token. The expiration time is 60 seconds.

### 3. Access protected view
Using some tool (for example httpie), do a GET request to http://localhost:8000/auth/protected, indicating the previous token as the value for the authorization header:
```
pip install httpie
http localhost:8000/auth/protected authorization:<tokenvalue>
```
HTTP 200 - `Hi <username>!` should be the response until token is expired.
