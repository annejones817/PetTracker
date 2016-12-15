from flask import render_template, request, redirect, url_for as url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database import session, User, Pet 

from . import app 

@app.route("/")
def index():
    return app.send_static_file("html/index.html")

@app.route("/static/html/signIn.html", methods = ["GET"])
def login_get():
	return app.send_static_file("html/signIn.html")

@app.route("/static/html/signIn.html", methods=["POST"]) 
def login_post(): 
	first_name = request.form["first-name"]
	last_name = request.form["last-name"]
	email = request.form["email"]
	password = request.form["password"]
	user = session.query(User).filter_by(email=email).first()

	if not user: 
		print("new user")
		user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
		session.add(user)
		session.commit()
		return redirect("http://0.0.0.0:8080/static/html/dashboard.html")

	if not check_password_hash(user.password, password):
		print("wrong password")
		flash("Incorrect username or password", "danger")
		return redirect(url_for("login_get"))

	login_user(user)
	print("user logged in")
	return redirect("http://0.0.0.0:8080/static/html/dashboard.html")	

@app.route("/logout")
def logout(): 
	logout_user();
	flash("Successfully logged out.")
	return redirect("http://0.0.0.0:8080/")	