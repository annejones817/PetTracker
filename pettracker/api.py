from flask import render_template, request, redirect, url_for as url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database import session, User, Pet 
from . import decorators

from . import app 

@app.route("/api/pets", methods=["GET"])
@decorators.accept("application/json")
def pets_get(): 
	"""Get list of pets"""

	#Get owner id
	data = request.json
	print(data)
	owner_email = data.owner_email
	owner_id = session.query(database.User.id).filter_by(User.email == owner_email)
	pets = session.query(database.Pet).filter_by(Pet.owner_id==owner_id)

	if not pets: 
		message = "No pets for this owner"
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")

	data = json.dumps([pet.as_dictionary for pet in pets])	
	print(data)
	return Response(data, 200, mimetype="application/json")

	#convert pets to JSON and return response
	data = json.dumps([pet.as_dictionary() for pet in pets])
	return Response(data, 200, mimetype="application/json")
