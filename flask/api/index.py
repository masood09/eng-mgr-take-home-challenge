from os import environ
from flask import Flask, jsonify, abort

from api.models import UserModel, UserSchema, WorkedHourModel, WorkedHourSchema

app = Flask(__name__)

from api.database import initialize_db

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

initialize_db(app)

users_schema = UserSchema(many=True)
worked_hours_schema = WorkedHourSchema(many=True)

# A route to list all the users in the system.
@app.route('/v1/users')
def user_list():
    # Let's get all the users here.
    all_users = UserModel.query.all()

    # Let's return the user list as JSON.
    return jsonify(users_schema.dump(all_users))


# A route to list all the worked hours for a user.
@app.route('/v1/users/<user_id>/worked_hours')
def worked_hours_list(user_id):
    # Let's get the user from database.
    user = UserModel.query.get(user_id)

    if user is None:
        # The user does not exist. Let's throw 404.
        abort(404)

    user_worked_hours = WorkedHourModel.query.filter_by(user_id = user_id).all()
    return jsonify(worked_hours_schema.dump(user_worked_hours))
