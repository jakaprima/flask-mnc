from flask import Blueprint, request, jsonify, make_response
from werkzeug import datastructures

from app.account.form import UserForm
from app.models import Users
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import load_user
from datetime import datetime
from app.utils.update_dict import update_dict


account = Blueprint('account', __name__)

@account.route('/profile', methods=['PUT'])
@jwt_required()
def user_update():
    # 7. Update Profile
    user_id = get_jwt_identity()
    user = load_user(user_id)
    user.update(**request.json)
    user.save()
    user.reload()
    result = user.to_mongo()
    result['user_id'] = result.pop('_id')
    result['updated_date'] = datetime.strftime(result['updated_date'], '%Y-%m-%d %H:%M:%S')
    keys_to_remove = ["pin", "balance", "created_date", "phone_number"]
    update_dict(result, keys_to_remove)
    response = {
        "status": "SUCCESS",
        "result": result
    }

    return make_response(jsonify(response)), 200
