import json
import pytest
from flask import g, request
from flask import session, json
from app.models.user import Users
from tests.fixtures import client, client_user

def test_success_update_profile(client, app, base_url):
    data_update_dict ={
        "first_name": "Tom",
        "last_name": "Araya",
        "address": "Jl. Diponegoro No. 215"
    }
    # create user
    data_create_dict = {
        "first_name": "Guntur",
        "last_name": "Saputro",
        "phone_number": "0811255501",
        "address": "Jl. Kebon Sirih No. 1",
        "pin": "123456"
    }
    user = Users.objects(phone_number=data_create_dict['phone_number'])
    if user:
        user = user.first()
    else:
        user = Users(**data_create_dict).save()

    user = Users(**data_create_dict).save()
    print('suer id', user.id)
    token = client_user(user, client)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    data = json.dumps(data_update_dict)
    response = client.put(base_url + "profile", data=data, content_type='application/json', headers=headers)
    response_data = json.loads(response.data)
    print('response', response_data['result'])

    assert response.status_code == 200
    for key in response_data['result']:
        if key in data_update_dict:
            assert response_data['result'][key] == data_update_dict[key]
