from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
import os
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
from models import UserForm, RegisterForm
from database import sqlite_connection

# Load variables from .env file
load_dotenv()

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLITE_DATABASE_URI")

# Database setup
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid Email or Password'}), 401
        
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
        
        response = make_response(redirect(url_for('home')))
        response.set_cookie('jwt_token', token)

        return response
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        existing_user = RegisterForm.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists. Please login.', 'warning')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        new_user = RegisterForm(public_id=str(uuid.uuid4()), email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
    form = UserForm()
    if request.method == 'POST':
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        birthdate = form.birthdate.data
        
        sql_script = f'''INSERT INTO users
                            (firstname, lastname, email, phone, birthdate)
                        VALUES (?, ?, ?, ?, ?)
                    '''
        conn, cursor_obj = sqlite_connection()
        cursor_obj.execute(sql_script, (firstname, lastname, email, phone, birthdate))
        conn.commit()

        # Close the connection
        conn.close()
        return redirect(url_for('form'))
    else:
        return render_template('form.html', form=form)
        
@app.route("/users")
def get_user():
    conn, cursor_obj = sqlite_connection()
    cursor_obj.execute('''SELECT * FROM users;''')
    users = cursor_obj.fetchall()
    return render_template('users.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)