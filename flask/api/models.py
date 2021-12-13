from marshmallow_sqlalchemy import auto_field

from api.database import db, ma

class WorkedHourModel(db.Model):
    # The table name as present in the provided schema.
    __tablename__ = 'worked_hours'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    date = db.Column(db.Date, nullable=False, primary_key=True)
    hours = db.Column(db.Numeric(4,2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

class WorkedHourSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        strict = True
        # We only want to expose certain fields in the API.
        fields = ("id", "date", "hours")
        model = WorkedHourModel

    # In the DB we are using user_id field name, in the API response we will use id. 
    id = auto_field("user_id", dump_only=True)

class UserModel(db.Model):
    # The table name as present in the provided schema.
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    worked_hours = db.relationship('WorkedHourModel',
        uselist=False,
        primaryjoin="UserModel.id == WorkedHourModel.user_id"
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # We only want to expose certain fields in the API.
        fields = ("id", "first_name", "last_name", "email")
        model = UserModel
