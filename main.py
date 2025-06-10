from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv
from models import UserForm
from database import sqlite_connection
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
        return render_template('index.html', form=form)
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
