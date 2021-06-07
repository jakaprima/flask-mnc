from flask import (
    Blueprint,
    request,
    jsonify,
    make_response
)
from flask_login import login_user
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug import datastructures
from app.account.form import UserForm
from app.auth.form import LoginForm
from app.models import Users
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    data_list = list(request.json.items())
    request.form = datastructures.MultiDict(data_list)
    form = UserForm(request.form)

    if form.validate():
        user = Users(
            **form.data
        ).save()
        print('date', user.created_date)

        data = form.data
        data.pop('pin')
        data['user_id'] = user.id
        data['created_date'] = datetime.strftime(user.created_date, '%Y-%m-%d %H:%M:%S')
        response = {
            'status': "success",
            'result': data
        }
        return make_response(jsonify(response)), 200
    # change format errors like requirement
    response = {}
    print('error', form.errors)
    for i, key in enumerate(form.errors):
        if key == 'phone_number':
            response['message'] = form.errors[key][0]['message']
        else:
            response[key] = form.errors[key][0]['message']

    return make_response(jsonify(response)), 400

@auth.route('/login', methods=['POST'])
def login():
    """Log in an existing user."""
    data_list = list(request.json.items())
    request.form = datastructures.MultiDict(data_list)
    form = LoginForm(request.form)
    if form.validate():
        user = Users.objects(pin=form.data['pin'], phone_number=form.data['phone_number']).first()
        if user is not None:
            login_user(user, remember=True)
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            result = {
                "status": "SUCCESS",
                "result": {
                    "access_token": f"{access_token}",
                    "refresh_token": f"{refresh_token}"
                }
            }
            return make_response(jsonify(result)), 200
        else:
            result = {
                "message": "Phone number and pin doesn’t match."
            }
            return make_response(jsonify(result)), 400

    return form.errors

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
