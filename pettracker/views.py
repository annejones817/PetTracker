from flask import render_template, request, redirect, url_for as url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database import session, User, Pet 

from . import app 

@app.route("/")
def index():
    return app.send_static_file("html/index.html")

@app.route("/login", methods = ["GET"])
def login_get():
	return app.send_static_file("html/signIn.html")

@app.route("/login", methods=["POST"]) 
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
		return redirect(url_for("dashboard_get"))

	if not check_password_hash(user.password, password):
		print("wrong password")
		flash("Incorrect username or password", "danger")
		return redirect(url_for("login_get"))

	login_user(user)
	print("user logged in")
	return redirect(url_for("dashboard_get"))	

@app.route("/dashboard")
def dashboard_get(): 
	return app.send_static_file("html/dashboard.html")	

@app.route("/logout")
def logout(): 
	logout_user();
	flash("Successfully logged out.")
	print("Successfully logged out.")
	return redirect(url_for("index"))	

@app.route("/add-pet", methods = ["GET"])
def add_pet_get(): 
	return app.send_static_file("html/addPet.html")

@app.route("/more-details/<int:id>")
def more_details_get(id): 
	return app.send_static_file("html/petDetailsPage.html")	


