import os.path
import json 

from flask import Response, jsonify, render_template, request, redirect, url_for as url_for, flash, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .database import session, User, Pet, Vet, Appointment, Vaccine, Medication, Food, Record 
from . import decorators
from .utils import upload_path
from .nocache import nocache
from .config import DevelopmentConfig

from . import app 



"""
@app.after_request
def add_header(response):
   
   Add headers to both force latest IE rendering engine or Chrome Frame,
   and also to cache the rendered page for 10 minutes.
  
   response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
   response.headers['Cache-Control'] = 'public, max-age=0'
   return response
"""   

@app.route("/api/pets", methods=["GET"])
@decorators.accept("application/json")
@nocache
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


@app.route("/api/add-pet", methods = ["POST"])
def add_pet_post(): 
	data = request.json
	pet_name = data["pet-name"]
	pet_birthdate = data["pet-birthdate"]
	owner_id = current_user.id

	pet = Pet(name=pet_name, birthdate=pet_birthdate, owner_id=owner_id)
	session.add(pet)
	session.commit()
	message="Pet added successfully"
	data=json.dumps({"message": message})
	return Response(data, 200, mimetype="application/json")

@app.route("/api/update-pet", methods = ["POST"])
def update_pet_post(): 
	data = request.json
		

@app.route("/uploads/<filename>", methods = ["GET"])
def uploaded_file(filename):	
	return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods = ["POST"])
def file_post():
	file = request.files.get("file")

	if not file: 
		data = {"message": "Could not find file data."}
		return Response(json.dumps(data), 422, mimetype="application/json")	

	file_name = secure_filename(file.filename)
	
	#Do these three lines in a separate call to a new route 
	record = Record(file_name=file_name, file_path="", pet_id = 2)
	session.add(record)
	session.commit()
	
	# Leave this line here
	file.save(upload_path(file_name))

	data = record.as_dictionary()
	return Response(json.dumps(data), 201, mimetype="application/json")

@app.route("/api/delete-pet/<int:id>", methods = ["POST"])
def delete_pet(id): 
	pet = session.query(Pet).filter(Pet.id==id).first()

	if not pet: 
		message = "Could not find pet with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")

	session.delete(pet)
	session.commit()

	message = "Pet deleted successfully"
	data = json.dumps({"message": message})	
	return Response(data, 200, mimetype="application/json")

@app.route("/more-details/api/more-details/<int:id>", methods = ["GET"])
def get_details(id): 
	pet = session.query(Pet).filter(Pet.id==id).first()
	#basicDetails = json.dumps(pet.as_dictionary())

	vet_id = pet.vet_id
	vet = session.query(Vet).filter(Vet.id==vet_id).first()
	#vetDetails = json.dumps(vet.as_dictionary())

	if not pet: 
		message = "Could not find pet with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")

	data = json.dumps([pet.as_dictionary(), vet.as_dictionary()])
	return Response(data, 200, mimetype="application/json")


		

