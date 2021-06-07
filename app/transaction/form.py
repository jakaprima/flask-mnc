from wtforms.fields import (
    StringField,
    IntegerField
)
from wtforms.validators import InputRequired, Length
from wtforms import Form
from app.models import Users


class TopupForm(Form):
    amount = IntegerField('Amount', validators=[InputRequired()])


class PaymentForm(Form):
    amount = IntegerField('Amount', validators=[InputRequired()])
    remarks = StringField('Remarks', validators=[Length(0, 200)])

class TransferForm(Form):
    target_user = StringField('Target User', validators=[InputRequired()])
    amount = IntegerField('Amount', validators=[InputRequired()])
    remarks = StringField('Remarks', validators=[Length(0, 200)])

    def validate_target_user(self, field):
        if Users.objects(user_id=field.data).first():
            raise ValidationError({"message": "User not exists"})



