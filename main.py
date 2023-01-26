# from alembic import command
# from alembic.config import Config
# from flask_script import Manager
from bcrypt import hashpw, checkpw, gensalt
import bcrypt
from flask import json
from flask import Flask, request, Response, jsonify, render_template, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from functools import wraps
from sqlalchemy import cast

# import models
from flask_migrate import Migrate


load_dotenv('.env')

# from .models import Message, Like, User


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.LargeBinary(60), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(140))
    likes = db.Column(db.Integer, default=0)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("pages/signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        print(username, password)
        user = User.query.filter_by(username=username).first()
        print(user, "checking user")
        if user is not None:
            return render_template("pages/signup.html", error="User already exists")
        user = User(username, password)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up.')
        return render_template("pages/login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("POST")
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        user = User.query.filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            session['username'] = username
            flash('You have successfully logged in.')
            return redirect(url_for('home'))
        else:
            flash('Error: Invalid username or password')

            return render_template('pages/login.html')
    return render_template('pages/login.html')


@ app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('index'))


@ app.route("/", methods=["POST", "GET"])
@ login_required
def home():
    if request.method == "GET":

        return render_template("pages/home.html", username=username)


@ app.route("/new-message", methods=["POST"])
def new_message():
    message = request.form.get("message")
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    message = Message(user_id=user.id, message=message)
    db.session.add(message)
    db.session.commit()
    return redirect("/")
