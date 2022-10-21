from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def init():

	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'vornok334'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
	db.init_app(app)

	from .auth import auth
	from .views import views

	app.register_blueprint(views, url_prefix="")
	app.register_blueprint(auth, url_prefix="")

	from .models import User

	createDB(app)

	login_manager = LoginManager()
	login_manager.login_view = "auth.login"
	login_manager.init_app(app)

	#defines how we access the user
	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app

def createDB(app):
	if not path.exists("website/user.db"):
		db.create_all(app=app)
		print("Database Created!")

