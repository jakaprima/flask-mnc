import pytest
import json
from flask.testing import FlaskClient
from dotenv import dotenv_values
env_list = dotenv_values()


@pytest.fixture
def api_client():
    return FlaskClient()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def client_user(user, client):
    base_url = env_list['BASE_URL']
    data_dict = {
        "phone_number": user.phone_number,
        "pin": user.pin
    }
    data = json.dumps(data_dict)
    response = client.post(base_url + "/login", data=data, content_type='application/json')
    response_data = json.loads(response.data)
    token = response_data['result']['access_token']
    return token