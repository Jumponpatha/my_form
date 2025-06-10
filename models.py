from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    birthdate = DateField('Data of Birhth', format='%Y-%m-%d', validators=[InputRequired()])