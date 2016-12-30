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
	pet_id = data["pet-id"]
	pet_name = ''
	pet_birthdate = ''
	vet_id = ''
	vet_name = ''
	vet_phone = ''
	vet_email = ''
	food_name = ''
	cups_per_day = ''
	basic = False
	vet = False
	food = False
	pet = session.query(Pet).filter(Pet.id == pet_id).first()
	message = ''


	if (data["pet-name"] != ''): 
		pet_name = data["pet-name"]
		basic = True
	if (data["pet-birthdate"] != ''): 
		pet_birthdate = data["pet-birthdate"]
		basic = True
	if (data["vet-name"] != ''): 
		vet_name = data["vet-name"]
		vet = True
	if (data["vet-phone"] != ''): 
		vet_phone = data["vet-phone"]	
		vet = True
	if (data["vet-email"] != ''): 
		vet_email = data["vet-email"]
		vet = True
	if (data["food-name"] != ''): 
		food_name = data["food-name"]	
		food = True
	if (data["cups-per-day"] != ''): 
		cups_per_day = data["cups-per-day"]	
		food = True	

	#Update basic pet info
	if (basic == True): 
		if (pet_name != ''):
			pet.name = pet_name
		if (pet_birthdate != ''): 
			pet.birthdate = pet_birthdate
		session.add(pet)
		session.commit()
		message += "Basic pet info updated. "	

	#Update vet info 
	if (vet == True): 
		#get current vet
		current_vet = session.query(Vet).join(Pet).filter(Pet.id==pet_id).first()
		if (current_vet and current_vet.vet_name == vet_name):
			if (vet_phone != ''): 
				current_vet.vet_phone = vet_phone
			if (vet_email != ''):
				current_vet.vet_email = vet_email 
			session.add(current_vet)
			session.commit()
			message += "Vet info updated. "
		else:
			#Check whether vet exists in DB
			vet_in_db = session.query(Vet).filter(Vet.vet_name==vet_name).first()
			if (vet_in_db): 
				pet.vet_id = vet_in_db.id
				session.add(pet)
				session.commit()
				message += "Vet info updated. "
			else: 
				vet = Vet(vet_name = vet_name, vet_phone = vet_phone, vet_email = vet_email)
				session.add(vet)
				session.commit()
				new_vet = session.query(Vet).filter(Vet.vet_name == vet.vet_name).first()
				pet.vet_id = new_vet.id
				message += "Vet info updated. "
	#Update food info
	if (food == True):
		current_food = session.query(Food).filter(Food.pet_id == pet_id).first()
		if (current_food):	
			if (food_name != ''):
				current_food.food_name = food_name
			if (cups_per_day != ''): 
				current_food.cups_per_day = cups_per_day
			session.add(current_food)
			session.commit()
			message += "Food info updated. "	
		else: 
			new_food = Food(food_name = food_name, cups_per_day = cups_per_day, pet_id = pet_id)
			session.add(new_food)
			session.commit()
			message += "Food info updated. "	

	data=json.dumps({"message": message})
	return Response(data, 200, mimetype="application/json")	



					

				



@app.route("/uploads/<filename>", methods = ["GET"])
def uploaded_file(filename):	
	return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods = ["POST"])
def file_post():
	file = request.files.get("file")
	pet_id = request.form.get("file-pet-id")

	if not file: 
		data = {"message": "Could not find file data."}
		return Response(json.dumps(data), 422, mimetype="application/json")	

	file_name = secure_filename(file.filename)
	
	record = Record(file_name=file_name, file_path="", pet_id = pet_id)
	session.add(record)
	session.commit()
	
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

	food = session.query(Food).filter(Food.pet_id==pet.id).first()

	if not pet: 
		message = "Could not find pet with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")
	if (vet and food): 
		data = json.dumps([pet.as_dictionary(), vet.as_dictionary(), food.as_dictionary()])
		
	elif (vet):
		data = json.dumps([pet.as_dictionary(), vet.as_dictionary()])
	elif (food): 
		data = json.dumps([pet.as_dictionary(), {}, food.as_dictionary()])
	else: 	
		data = json.dumps([pet.as_dictionary()])

	return Response(data, 200, mimetype="application/json")


		

