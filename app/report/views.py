from flask import Blueprint, request, jsonify, make_response
from werkzeug import datastructures
from app.models import Users, Topup, Payment
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import load_user
from datetime import datetime
from app.utils.update_dict import update_dict


report = Blueprint('report', __name__)


@report.route('/report', methods=['GET'])
@jwt_required()
def report_list():
    # 6. Report Transactions
    """
    {
    "status": "SUCCESS"
    "result": [
        {
            "transfer_id": "a7d39cf6-44b6-41fc-b3e9-
            7b16df5321c5",
            "status": "SUCCESS",
            "user_id": "bc1c823e-b0fb-4b20-88c0-
            dff25e283252",
            "transaction_type": "DEBIT",
            "amount": 30000,
            "remarks": "Hadiah Ultah"
            "balance_before": 400000,
            "balance_after": 370000,
            "created_date": "2021-04-01 22:23:20"
        }, {

            "payment_id": "13bcb11c-111e-4a65-9afd-
            90a86a01cd21",

            "status": "SUCCESS",
            "user_id": "bc1c823e-b0fb-4b20-88c0-
            dff25e283252",
            "transaction_type": "DEBIT",
            "amount": 10000,
            "remarks": "Pulsa Telkomsel 100k"
            "balance_before": 500000,
            "balance_after": 400000,
            "created_date": "2021-04-01 22:22:00"
        }, {
            "top_up_id": "201ddde1-f797-484b-b1a0-
            07d1190e790a",
            "status": "SUCCESS",
            "user_id": "bc1c823e-b0fb-4b20-88c0-
            dff25e283252",
            "transaction_type": "CREDIT",
            "amount": 500000,
            "remarks": "",
            "balance_before": 0,
            "balance_after": 500000,
            "created_date": "2021-04-01 22:21:21"
        }
    ]
    """
    user_id = get_jwt_identity()
    user = Users.objects.get(user_id=user_id)
    topup_list = Topup.objects(user_id=user_id)
    payment_list = Payment.objects(user_id=user_id)
    transfer_list = None
    result = []
    topup_list_result = []
    payment_list_result = []
    for data in topup_list:
        data = data.to_mongo()
        data['top_up_id'] = data.pop('_id')
        data['remarks'] = data.get('remarks', '')
        data.pop('_cls')

        data['created_date'] = datetime.strftime(data['created_date'], '%Y-%m-%d %H:%M:%S')
        topup_list_result.append(data)

    for data in payment_list:
        data = data.to_mongo()
        data['payment_id'] = data.pop('_id')
        data['created_date'] = datetime.strftime(data['created_date'], '%Y-%m-%d %H:%M:%S')
        payment_list_result.append(data)


    result.append(topup_list_result)
    result.append(payment_list_result)

    response = {
        "status": "SUCCESS",
        "result": result
    }
    return response
