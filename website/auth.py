from flask import Blueprint, render_template, url_for, request, flash, redirect
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/log-in", methods=['GET', 'POST'])
def logIn():

	if request.method == 'POST':

		username = request.form.get("username")
		password = request.form.get("password")

		username_exists = User.query.filter_by(username=username).first()

		if username_exists:
			if check_password_hash(username_exists.password, password):
				flash('Login Successful!', category='success')
				login_user(username_exists, remember=True)
				return redirect(url_for("views.home"))
			else:
				flash('Password is incorrect.', category='error')
		else:
			flash('Username does not exist.', category='error')

	return render_template("login.html")

@auth.route("/sign-up", methods=['GET', 'POST'])
def signUp():

	if request.method == 'POST':	
		#retrieve form data
		email = request.form.get("email")
		username = request.form.get("username")
		password = request.form.get("password1")
		confirm = request.form.get("password2")

		#check if data exists in db
		email_exists = User.query.filter_by(email=email).first()
		username_exists = User.query.filter_by(username=username).first()

		#add email verification here
		#placeholder code
		if email_exists:
			flash('Email already exists.', category='error')
		elif len(username) == 0:
			flash('Please enter a username.', category='error')
		elif username_exists:
			flash('Username has been taken.', category='error')
		elif password != confirm:
			flash('Passwords do not match.', category='error')
		elif len(username) < 3:
			flash('Username must be minimum 3 charecters.', category='error')
		elif len(password) < 8:
			flash('Password must be minimum 8 charecters.', category='error')
		elif len(email) < 5:
			flash('Email is invalid.', category='error')
		else:
			newUser = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
			db.session.add(newUser)
			db.session.commit()
			login_user(newUser, remember=True)
			flash('User Created!', category='success')
			return redirect(url_for('views.home'))

	return render_template("signup.html")

@auth.route("/sign-out")
@login_required
def signOut():
	logout_user()
	return render_template(url_for("views.home"))