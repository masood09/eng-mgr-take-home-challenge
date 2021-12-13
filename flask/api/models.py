from api.database import db, ma

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

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # We only want to expose certain fields in the API.
        fields = ("id", "first_name", "last_name", "email")
        model = UserModel
