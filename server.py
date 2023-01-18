from flask import json
from flask import Flask, request, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/dbname'
# db = SQLAlchemy(app)
db = 'test'


@app.route("/")
def index():
    return render_template('index.html', info='test')


if __name__ == '__main__':
    app.run(debug=True)
