from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

#route is restricted to only logged in users
@views.route("/")
@views.route("/home")
@login_required
def home():
	return render_template("home.html", name=current_user.username)
