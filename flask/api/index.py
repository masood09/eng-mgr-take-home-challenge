from os import environ
from datetime import datetime
from flask import Flask, jsonify, abort, request

from api.models import UserModel, UserSchema, WorkedHourModel, WorkedHourSchema

app = Flask(__name__)

from api.database import initialize_db, db

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

initialize_db(app)

users_schema = UserSchema(many=True)
worked_hour_schema = WorkedHourSchema()
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


# A route to create a worked hour for a user.
@app.route('/v1/users/<user_id>/worked_hours', methods=['POST'])
def create_worked_hour(user_id):
    # Let's get the user.
    user = UserModel.query.get(user_id)

    if user is None:
        # User does not exist. Throw 404.
        abort(404)

    # Let's get the body params (date and hours)
    worked_date_request = request.json.get('date', None)
    hours_request = request.json.get('hours', None)

    if worked_date_request is None or hours_request is None:
        return jsonify({"error": "Both hours and date are required in the request body"}), 400

    try:
        # Let's convert the date to Python object.
        worked_date = datetime.strptime(worked_date_request, "%Y-%m-%d").date()
    except ValueError as exception:
        # Well the date passed in the body does look formatted. Let's throw Bad request.
        return jsonify({"error": "Invalid date"}), 400

    try:
        hours = float(hours_request)
    except ValueError as exception:
        # Well we were not able to convert the hours in body to float.
        return jsonify({"error": "Invalid hours"}), 400

    if hours < 0 or hours > 24:
        # The hours are not between 0 and 24.
        return jsonify({"error": "Invalid hours"}), 400

    worked_hour = WorkedHourModel()
    worked_hour.user_id = user_id
    worked_hour.hours = hours
    worked_hour.date = worked_date

    db.session.add(worked_hour)

    try:
        # Let's save the record to the DB.
        db.session.commit()
    except:
        # Something happened (most likely IntegrityError). Let's send Bad request.
        # TODO: Catch sqlalchemy.exc.IntegrityError seperately.
        return jsonify({"error": "A error occured while saving - please verify if hours for the date alreay entered."}), 400

    return worked_hour_schema.jsonify(worked_hour), 201
