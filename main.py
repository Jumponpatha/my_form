from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv
from models import UserForm
# Load variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

CORS(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
    form = UserForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        birthdate = form.birthdate.data
        return f'''First Name: {firstname} <br> Last Name: {lastname} <br> Email: {email} 
        <br> Phone: {phone} <br> Birthdate: {birthdate}'''
    return render_template('index.html', form=form)
        


if __name__ == "__main__":
    app.run(debug=True)
