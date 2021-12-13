from os import environ
from flask import Flask, jsonify

from api.models import UserModel, UserSchema

app = Flask(__name__)

from api.database import initialize_db

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

initialize_db(app)

users_schema = UserSchema(many=True)

# A route to list all the users in the system.
@app.route('/v1/users')
def user_list():
    # Let's get all the users here.
    all_users = UserModel.query.all()

    # Let's return the user list as JSON.
    return jsonify(users_schema.dump(all_users))
