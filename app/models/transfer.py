from .. import db, login_manager
import datetime
import uuid
from .user import Users
from app.utils.choices import transaction_types, status

class Transfer(db.Document):
    transfer_id = db.StringField(default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id_from = db.ReferenceField(Users, required=True)
    user_id_to = db.ReferenceField(Users, required=True)
    amount = db.IntField(required=True)
    balance_before = db.IntField(default=0, required=True)
    balance_after = db.IntField(required=True)
    created_date = db.DateTimeField(default=datetime.datetime.utcnow())
    transaction_type = db.StringField(max_length=10, choices=transaction_types.keys(), required=True)
    status = db.StringField(max_length=10, choices=status.keys(), required=True)
    remarks = db.StringField(max_length=200)

    meta = {'allow_inheritance': True}