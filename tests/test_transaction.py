import json
import pytest
from flask import g, request
from flask import session, json
from app.models.user import Users
from tests.fixtures import client, client_user

def test_top_up(client, app, base_url):
    data_dict = {
        "amount": 2000
    }
    data_user = {
        "first_name": "Guntur",
        "last_name": "Saputro",
        "phone_number": "0811255501",
        "address": "Jl. Kebon Sirih No. 1",
        "pin": "123456"
    }
    user = Users.objects(phone_number=data_user['phone_number'])
    if user:
        user = user.first()
    else:
        user = Users(**data_user).save()
    token = client_user(user, client)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    data = json.dumps(data_dict)
    response = client.post(base_url + "top-up", data=data, content_type='application/json', headers=headers)
    response_data = json.loads(response.data)
    user.reload()

    assert response.status_code == 200
    assert response_data['result']['balance_after'] == user.balance

def test_success_payment(client, app, base_url):
    data_dict = {
        "amount": 1000,
        "remarks": "Pulsa Telkomsel 100k",
    }
    data_user = {
        "first_name": "Guntur",
        "last_name": "Saputro",
        "phone_number": "0811255501",
        "address": "Jl. Kebon Sirih No. 1",
        "pin": "123456"
    }
    user = Users.objects(phone_number=data_user['phone_number'])
    if user:
        user = user.first()
    else:
        user = Users(**data_user).save()
    token = client_user(user, client)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    data = json.dumps(data_dict)
    response = client.post(base_url + "pay", data=data, content_type='application/json', headers=headers)
    response_data = json.loads(response.data)
    user.reload()

    assert response.status_code == 200
    assert response_data['result']['balance_after'] == user.balance

def test_failed_payment(client, app, base_url):
    data_dict = {
        "amount": 100000000,
        "remarks": "Pulsa Telkomsel 100k",
    }
    data_user = {
        "first_name": "Guntur",
        "last_name": "Saputro",
        "phone_number": "0811255501",
        "address": "Jl. Kebon Sirih No. 1",
        "pin": "123456"
    }
    user = Users.objects(phone_number=data_user['phone_number'])
    if user:
        user = user.first()
    else:
        user = Users(**data_user).save()
    token = client_user(user, client)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    data = json.dumps(data_dict)
    response = client.post(base_url + "pay", data=data, content_type='application/json', headers=headers)
    response_data = json.loads(response.data)
    user.reload()

    assert response.status_code == 400

# def test_transfer(client, app, base_url):
#     """
#     {
#         "target_user": "b7342e8e-e8e7-4a5d-873e-b1b1bfcdeddb",
#         "amount": 30000,
#         "remarks": "Hadiah Ultah",
#     }
#     """
#     data_user = {
#         "first_name": "Guntur",
#         "last_name": "Saputro",
#         "phone_number": "0811255501",
#         "address": "Jl. Kebon Sirih No. 1",
#         "pin": "123456"
#     }
#     user = Users.objects(phone_number=data_user['phone_number'])
#     if user:
#         user = user.first()
#     else:
#         user = Users(**data_user).save()
#     data_dict =     {
#         "target_user": user.id,
#         "amount": 30000,
#         "remarks": "Hadiah Ultah",
#     }
#     token = client_user(user, client)
#     headers = {
#         'Authorization': 'Bearer {}'.format(token)
#     }
#
#     data = json.dumps(data_dict)
#     response = client.post(base_url + "transfer", data=data, content_type='application/json', headers=headers)
#     response_data = json.loads(response.data)
#     user.reload()
#
#     assert response.status_code == 200
#     assert response_data['result']['balance_after'] == user.balance
