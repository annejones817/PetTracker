import os.path
import json 

from flask import Response, render_template, request, redirect, url_for as url_for, flash
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
	owner_id = current_user.id
	pets = session.query(Pet).filter(Pet.owner_id==owner_id)

	if not pets: 
		message = "No pets for this owner"
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")

	#convert pets to JSON and return response
	data = json.dumps([pet.as_dictionary() for pet in pets])	
	return Response(data, 200, mimetype="application/json")

	

