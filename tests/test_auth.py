import json
import pytest
from flask import g, request
from flask import session, json
from app.models.user import Users
from tests.fixtures.client import client

def test_success_register(client, app, base_url):
    data_dict = {
        "first_name": "Guntur",
        "last_name": "Saputro",
        "phone_number": "0811255501",
        "address": "Jl. Kebon Sirih No. 1",
        "pin": "123456"
    }
    user = Users.objects(phone_number=data_dict['phone_number'])
    if user:
        user = user.delete()

    data = json.dumps(data_dict)
    response = client.post(base_url + "register", data=data, content_type='application/json')
    response_data = json.loads(response.data)
    print('aa', response_data)

    assert response.status_code == 200
    for key in response_data['result']:
        if key in data_dict:
            assert response_data['result'][key] == data_dict[key]

def test_fail_register(client, app, base_url):
    data_dict = {
        "first_name": "Guntur",
        "last_name": "Saputro",
        "phone_number": "0811255501",
        "address": "Jl. Kebon Sirih No. 1",
        "pin": "123456"
    }

    data = json.dumps(data_dict)
    response = client.post(base_url + "register", data=data, content_type='application/json')
    response_data = json.loads(response.data)

    assert response.status_code == 400
    assert response_data['message'] == 'Phone Number already registered'

def test_success_login(client, app, base_url):
    data_dict = {
        "phone_number": "0811255501",
        "pin": "123456"
    }
    data = json.dumps(data_dict)
    response = client.post(base_url + "login", data=data, content_type='application/json')
    response_data = json.loads(response.data)

    assert response.status_code == 200
    assert response_data['result']['access_token'] != None
    assert response_data['result']['refresh_token'] != None

def test_fail_login(client, app, base_url):
    data_dict = {
        "phone_number": "0811255501",
        "pin": "123fsdvs"
    }
    data = json.dumps(data_dict)
    response = client.post(base_url + "login", data=data, content_type='application/json')
    response_data = json.loads(response.data)

    assert response.status_code == 400
    assert response_data['message'] == 'Phone number and pin doesn’t match.'
