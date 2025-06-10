from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class UserForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    birthdate = DateField('Data of Birhth', format='%Y-%m-%d', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

