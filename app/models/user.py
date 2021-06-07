from flask_login import AnonymousUserMixin, UserMixin
import datetime
from .. import db, login_manager
import uuid

class Users(UserMixin, db.Document):
    user_id = db.StringField(default=lambda: str(uuid.uuid4()), primary_key=True)
    first_name = db.StringField(max_length=20)
    last_name = db.StringField(max_length=20)
    phone_number = db.StringField(max_length=11)
    address = db.StringField(max_length=100)
    pin = db.StringField(max_length=8)
    created_date = db.DateTimeField(default=datetime.datetime.utcnow())
    updated_date = db.DateTimeField(default=datetime.datetime.utcnow())
    balance = db.IntField(default=0)

    def full_name(self):
        return f"{self.first_name, self.last_name}"

    def __repr__(self):
        return f"{self.full_name()}"


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return Users.objects(user_id=user_id).first()