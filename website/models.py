from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#database model
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	username = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), default=func.now())
