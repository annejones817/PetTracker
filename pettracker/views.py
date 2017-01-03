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


