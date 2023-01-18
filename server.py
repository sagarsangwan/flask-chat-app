from flask import json
from flask import Flask, request, Response, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


load_dotenv('.env')

# from .models import Message, Like, User


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(140))
    likes = db.Column(db.Integer, default=0)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("pages/signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return render_template("pages/signup.html", error="User already exists")
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return render_template("pages/login.html")


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("pages/login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return render_template("pages/login.html", error="User does not exist")
        if user.password != password:
            return render_template("pages/login.html", error="Incorrect password")

        return render_template("pages/home.html", username=username)


@app.route("/new-message", methods=["POST"])
def new_message():
    message = request.form.get("message")
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    message = Message(user_id=user.id, message=message)
    db.session.add(message)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
