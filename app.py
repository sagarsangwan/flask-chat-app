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
    password = db.Column(db.String(255))
    date_of_registration = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, password, date_of_registration=None):

        self.username = username
        self.password = password
        if date_of_registration is not None:
            self.date_of_registration = date_of_registration
        else:
            self.date_of_registration = db.func.now()

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = bcrypt.hashpw(
    #         password.encode('utf-8'), bcrypt.gensalt())


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(140))
    likes = db.Column(db.Integer, default=0)
    time_of_msg = db.Column(db.DateTime, default=db.func.now())
    user = db.relationship('User', backref=db.backref(
        'messages', lazy='dynamic'))
    likes = db.relationship('Like', backref=db.backref(
        'messages'))

    def __repr__(self):
        return '<Message %r>' % self.message

    def __init__(self, user_id, message, likes, time_of_msg=None):
        self.user_id = user_id
        self.message = message
        self.likes = likes
        if time_of_msg is not None:
            self.time_of_msg = time_of_msg
        else:
            self.time_of_msg = db.func.now()

    def get_all_likes(self):
        return Like.query.filter_by(message_id=self.id).all()


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    user = db.relationship('User', backref=db.backref(
        'likes', lazy='dynamic'))
    message = db.relationship('Message', backref=db.backref(
        'likes', lazy='dynamic'))

    def __repr__(self):
        return '<Like %r>' % self.id

    def __init__(self, user_id, message_id):
        self.user_id = user_id
        self.message_id = message_id


def get_current_user_id():
    if 'username' in session:
        print(session['username'])
        user = User.query.filter_by(username=session['username']).first()
        return user.id
    return None


# @app.before_request
# def before_request():
#     g.user_id = get_current_user_id()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@ app.route("/", methods=["POST", "GET"])
@ login_required
def home():
    if request.method == "GET":
        # get all messages from db in order of latest first
        all_messages = Message.query.order_by(Message.time_of_msg.desc()).all()

        print(all_messages, "all messages")

        all_likes = Like.query.all()

        current_user = get_current_user_id()
        print(current_user, "current user")

        return render_template("pages/index.html", user=current_user, all_messages=all_messages, likes=all_likes)


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
        date_of_registration = db.func.now()
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
        if user and user.password == password:
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
    return redirect(url_for('login'))


@ app.route("/new-message", methods=["POST"])
def new_message():
    message = request.form.get("message")
    username = session['username']
    user = User.query.filter_by(username=username).first()
    message = Message(user_id=user.id, message=message, likes=0)

    db.session.add(message)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host="0.0.0.0", port=8000)
