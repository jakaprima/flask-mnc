import datetime
from .. import db, login_manager
import uuid
from .user import Users
from app.utils.choices import transaction_types, status

class Payment(db.Document):
    user_id = db.ReferenceField(Users, required=True)
    payment_id = db.StringField(default=lambda: str(uuid.uuid4()), primary_key=True)
    amount = db.IntField(required=True)
    remarks = db.StringField(max_length=200)
    balance_before = db.IntField(required=True)
    balance_after = db.IntField(required=True)
    created_date = db.DateTimeField(default=datetime.datetime.utcnow())
    transaction_type = db.StringField(max_length=10, choices=transaction_types.keys(), required=True)
    status = db.StringField(max_length=10, choices=status.keys(), required=True)
