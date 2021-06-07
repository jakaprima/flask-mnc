from flask import Blueprint, request, jsonify, make_response
from werkzeug import datastructures

from app.transaction.form import TopupForm, PaymentForm, TransferForm
from app.models import Users, Topup, Payment, Transfer
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import load_user
from datetime import datetime
from app.utils.update_dict import update_dict
from app.task.transfer import transfer_task
from app import q

transaction = Blueprint('transaction', __name__)

@transaction.route('/top-up', methods=['POST'])
@jwt_required()
def topup():
    user_id = get_jwt_identity()
    data_list = list(request.json.items())
    request.form = datastructures.MultiDict(data_list)
    form = TopupForm(request.form)

    if form.validate():
        data = form.data
        data['user_id'] = user_id
        topup_history = Topup.objects(user_id=user_id)
        amount = int(data.pop('amount'))
        if topup_history:
            latest_topup_history = topup_history[len(topup_history) - 1]
            print('latest_topup_history', latest_topup_history.id)
            balance_before = latest_topup_history.balance_after
            balance_after = balance_before + amount
        else:
            balance_before = 0
            balance_after = amount
        data['balance_before'] = balance_before
        data['balance_after'] = balance_after
        data['amount'] = amount
        data['transaction_type'] = data.get('transaction_type', 'CREDIT')
        data['status'] = 'SUCCESS'

        user = Users.objects.get(user_id=user_id)
        user.balance = balance_after
        user.save()

        instance = Topup(**data).save()

        result = instance.to_mongo()
        keys_to_remove = ["user_id", "_cls", "transaction_type"]
        update_dict(result, keys_to_remove)
        result['top_up_id'] = result.pop('_id')
        result['created_date'] = datetime.strftime(result['created_date'], '%Y-%m-%d %H:%M:%S')
        result['amount_top_up'] = result.pop('amount')
        status = result.pop('status')

        response = {
            "status": status,
            "result": result
        }
        return response
    return form.errors

@transaction.route('/pay', methods=['POST'])
@jwt_required()
def payment():
    user_id = get_jwt_identity()
    data_list = list(request.json.items())
    request.form = datastructures.MultiDict(data_list)
    form = PaymentForm(request.form)
    response = form.errors
    if form.validate():
        user = Users.objects.get(user_id=user_id)
        data = form.data
        data['user_id'] = user
        data['amount'] = int(data.pop('amount'))
        data['balance_before'] = user.balance
        data['balance_after'] = data['balance_before'] - data['amount']
        data['transaction_type'] = data.get('transaction_type', 'CREDIT')
        data['status'] = 'SUCCESS'

        if data['balance_after'] < 0:
            return make_response(jsonify({
                "message": "Balance is not enough"
            })), 400

        user = Users.objects.get(user_id=user_id)
        user.balance = data['balance_after']
        user.save()

        instance = Payment(**data).save()
        result = instance.to_mongo()
        keys_to_remove = ["user_id", "transaction_type"]
        update_dict(result, keys_to_remove)
        result['payment_id'] = result.pop('_id')
        result['created_date'] = datetime.strftime(result['created_date'], '%Y-%m-%d %H:%M:%S')
        status = result.pop('status')

        response = {
            "status": status,
            "result": result
        }
    return response

@transaction.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    user_id = get_jwt_identity()
    data_list = list(request.json.items())
    request.form = datastructures.MultiDict(data_list)
    form = TransferForm(request.form)
    response = form.errors
    if form.validate():

        data = {
            'user_id_from': user_id,
            'user_id_to': form.data['target_user'],
            'amount': form.data['amount'],
            'transaction_type': form.data.get('DEBIT', 'CREDIT'),
            'status': 'SUCCESS',
            'remarks': form.data.get('remarks')
        }
        result = transfer_task.delay(data)
        job = q.enqueue(transfer_task, data)
        
        q_len = len(q)
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in queue"

    return response
