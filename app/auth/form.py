from wtforms.fields import StringField
from wtforms.validators import InputRequired, Length
from wtforms import Form

class LoginForm(Form):
    pin = StringField(
        'Pin', validators=[InputRequired(),
                                    Length(6)])
    phone_number = StringField(
        'Phone Number', validators=[InputRequired(),
                                    Length(10, 11)])
