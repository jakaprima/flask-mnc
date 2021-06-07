from flask import url_for
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    IntegerField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from app.models import Users
from wtforms import ValidationError, Form

class UserForm(Form):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    phone_number = StringField(
        'Phone Number', validators=[InputRequired(),
                                 Length(1, 11)])
    address = StringField(
        'Address', validators=[InputRequired(),
                                    Length(1, 200)])
    pin = StringField(
        'Pin', validators=[InputRequired(),
                                    Length(8)])

    def validate_phone_number(self, field):
        if Users.objects(phone_number=field.data).first():
            raise ValidationError({"message": "Phone Number already registered"})

class LoginForm(Form):
    pin = StringField(
        'Pin', validators=[InputRequired(),
                                    Length(8)])
    phone_number = StringField(
        'Phone Number', validators=[InputRequired(),
                                    Length(1, 11)])

class TopupForm(Form):
    amount = IntegerField('Amount', validators=[InputRequired()])

class PaymentForm(Form):
    amount = IntegerField('Amount', validators=[InputRequired()])
    remarks = StringField('Remarks', validators=[Length(0, 200)])

