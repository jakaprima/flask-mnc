import time
from app.models import Users, Transfer
from app import celery

@celery.task()
def transfer_task(data):
    user_from = Users.objects.get(user_id=data.pop('user_id_from'))
    user_from_balance_before = user_from.balance
    user_from_balance_after = user_from_balance_before - int(data['amount'])
    target_user = Users.objects.get(user_id=data.pop('user_id_to'))
    target_user_balance_before = target_user.balance
    target_user_balance_after = target_user_balance_before + int(data['amount'])

    user_from.balance = user_from_balance_after
    user_from.save()
    target_user.balance = target_user_balance_after
    target_user.save()

    data['user_id_from'] = user_from
    data['user_id_to'] = target_user
    instance = Transfer(**data)

    return instance

