import os
from app.api.api_handler import api_request

api = os.getenv('API_ADDRESS_AUTH', 'localhost:5000')


def get_user():
    user = api_request(api, 'get-user', '')
    return user


def get_user_role():
    user_role = get_user()['role']
    return user_role
