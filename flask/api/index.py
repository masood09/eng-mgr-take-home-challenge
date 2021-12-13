from os import environ
from flask import Flask, jsonify

app = Flask(__name__)

from api.database import initialize_db

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

initialize_db(app)

@app.route('/')
def hello_world():
    return "Hello World"
