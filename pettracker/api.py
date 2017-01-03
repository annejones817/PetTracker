import os.path
import json 

from flask import Response, jsonify, render_template, request, redirect, url_for as url_for, flash, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .database import session, User, Pet, Vet, Appointment, Vaccine, Medication, Food, Record, Photo 
from . import decorators
from .utils import upload_path, upload_photo_path
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

@app.route("/api/join", methods=["POST"]) 
def signup_post(): 
	data = request.json
	first_name = data["first_name"]
	last_name = data["last_name"]
	email = data["email"]
	password = data["password"]
	user = session.query(User).filter(User.email==email).first()


	if not user: 
		user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
		session.add(user)
		session.commit()
		data = json.dumps({"message": "New user created successfully"})
		login_user(user)
		return Response(data, 201, mimetype="application/json")

	else: 
		data = json.dumps({"message": "User already exists"})
		return Response(data, 400, mimetype="application/json")	

@app.route("/api/login", methods=["POST"]) 
def login_post():	
	data = request.json	 
	print(data)
	email = data["email"]
	password = data["password"]
	user = session.query(User).filter(User.email==email).first()

	if not user: 
		data = json.dumps({"message": "Invalid email and/or password"})
		return Response(data, 422, mimetype="application/json")

	if not check_password_hash(user.password, password):
		data = json.dumps({"message": "Invalid email and/or password"})
		return Response(data, 422, mimetype="application/json")	

	else:
		login_user(user)
		data = json.dumps({"message": "Successful login"})
		return Response(data, 200, mimetype="application/json")	

@app.route("/api/profile-details", methods = ["GET"])
def profile_getDetails(): 
	user_id = current_user.id
	first_name = session.query(User.first_name).filter(User.id == user_id).first()	
	last_name = session.query(User.last_name).filter(User.id == user_id).first()	
	email = session.query(User.email).filter(User.id == user_id).first()	

	data = json.dumps({
			"first_name": first_name, 
			"last_name": last_name, 
			"email": email
		})

	return Response(data, 200, mimetype="application/json")		

@app.route("/api/pets", methods=["GET"])
@decorators.accept("application/json")
#@nocache
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
	record_type = request.form.get("record-type")
	record_details = request.form.get("record-details")

	if not file: 
		data = {"message": "Could not find file data."}
		return Response(json.dumps(data), 422, mimetype="application/json")	

	filename = secure_filename(file.filename)
	
	record = Record(record_type = record_type, record_details = record_details, file_name=filename, file_path="/uploads/" + filename, pet_id = pet_id)
	session.add(record)
	session.commit()
	
	file.save(upload_path(filename))

	data = record.as_dictionary()
	return Response(json.dumps(data), 201, mimetype="application/json")

@app.route("/photos/<filename>", methods = ["GET"])
def uploaded_photo(filename):	
	return send_from_directory(upload_photo_path(), filename)

@app.route("/api/photos", methods = ["POST"])
def photo_post(): 
	file = request.files.get("photo")
	pet_id = request.form.get("photo-pet-id")

	if not file: 
		data = {"message": "Could not find photo data."}
		return Response(json.dumps(data), 422, mimetype="application/json")

	currentPhoto = session.query(Photo).filter(Photo.pet_id==pet_id).first()
	if currentPhoto: 
		session.delete(currentPhoto)
		session.commit()	

	filename = secure_filename(file.filename)

	photo = Photo(file_name=filename, file_path="/photos/" + filename, pet_id = pet_id)
	session.add(photo)
	session.commit()

	file.save(upload_photo_path(filename))

	data = photo.as_dictionary()
	return Response(json.dumps(data), 201, mimetype="application/json")		

@app.route("/api/get-photo/<int:id>", methods = ["GET"])
def photo_get(id): 	
	photoFile = session.query(Photo.file_name).filter(Photo.pet_id == id).first()
	
	if not photoFile: 
		data = {"message": "No photo", "id": id}
		return Response(json.dumps(data), 200, mimetype="application/json")

	data = {"message": "Photo", "src": photoFile, "id": id}
	return Response(json.dumps(data), 200, mimetype="application/json")

@app.route("/api/delete-pet/<int:id>", methods = ["POST"])
def delete_pet(id): 
	pet = session.query(Pet).filter(Pet.id==id).first()
	records = session.query(Record).filter(Record.pet_id==id).all()
	photo = session.query(Photo).filter(Photo.pet_id==id).first()

	if not pet: 
		message = "Could not find pet with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")

	session.delete(pet)
	session.delete(photo)
	for record in records:
		session.delete(record)


	session.commit()

	message = "Pet deleted successfully"
	data = json.dumps({"message": message})	
	return Response(data, 200, mimetype="application/json")


@app.route("/more-details/api/more-details/<int:id>", methods = ["GET"])
def get_details(id): 
	data = {}

	pet = session.query(Pet).filter(Pet.id==id).first()

	vet_id = pet.vet_id
	vet = session.query(Vet).filter(Vet.id==vet_id).first()

	food = session.query(Food).filter(Food.pet_id==pet.id).first()

	records = session.query(Record).filter(Record.pet_id == pet.id).all()

	photo = session.query(Photo.file_name).filter(Photo.pet_id == pet.id).first()

	if not pet: 
		message = "Could not find pet with id {}".format(id)
		data["message"] = message
		data = json.dumps(data)
		return Response(data, 404, mimetype="application/json")

	if pet: 
		data["pet"] = pet.as_dictionary()
	if vet: 
		data["vet"] = vet.as_dictionary()
	if food: 
		data["food"] = food.as_dictionary()
	if records: 
		data["records"] = [record.as_dictionary() for record in records]
	if photo: 
		data["photo"] = photo			

	return Response(json.dumps(data), 200, mimetype="application/json")				
		
@app.route("/more-details/api/delete-record-<int:id>", methods = ["POST"])
def delete_record(id): 
	record = session.query(Record).filter(Record.id==id).first()

	if not record: 
		message = "Could not find record with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")

	session.delete(record)
	session.commit()

	message = "Record deleted successfully"
	data = json.dumps({"message": message})	
	return Response(data, 200, mimetype="application/json")
