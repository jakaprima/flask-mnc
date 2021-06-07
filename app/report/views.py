from flask import Blueprint, request, jsonify, make_response
from werkzeug import datastructures
from app.models import Users, Topup, Payment, Transfer
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import load_user
from datetime import datetime
from app.utils.update_dict import update_dict


report = Blueprint('report', __name__)


@report.route('/report', methods=['GET'])
@jwt_required()
def report_list():
    user_id = get_jwt_identity()
    user = Users.objects.get(user_id=user_id)
    topup_list = Topup.objects(user_id=user_id)
    payment_list = Payment.objects(user_id=user_id)
    transfer_list = Transfer.objects(user_id_from=user_id)
    result = []
    for data in topup_list:
        data = data.to_mongo()
        data['top_up_id'] = data.pop('_id')
        data['remarks'] = data.get('remarks', '')
        data.pop('_cls')

        data['created_date'] = datetime.strftime(data['created_date'], '%Y-%m-%d %H:%M:%S')
        result.append(data)

    for data in payment_list:
        data = data.to_mongo()
        data['payment_id'] = data.pop('_id')
        data['created_date'] = datetime.strftime(data['created_date'], '%Y-%m-%d %H:%M:%S')
        result.append(data)

    for data in transfer_list:
        data = data.to_mongo()
        data['created_date'] = datetime.strftime(data['created_date'], '%Y-%m-%d %H:%M:%S')
        result.append(data)

    response = {
        "status": "SUCCESS",
        "result": result
    }
    return response
