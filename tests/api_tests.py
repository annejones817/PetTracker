import unittest
import os
import shutil
import json
import uuid
from flask import Flask, current_app
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO, BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

import sys; print(list(sys.modules.keys()))

os.environ["CONFIG_PATH"] = "pettracker.config.TestingConfig"

from pettracker import app
from pettracker.database import *
from pettracker.api import * 
from pettracker.utils import upload_path, upload_photo_path



class TestAPI(unittest.TestCase): 
	"""Tests for the pettracker API"""
	def setUp(self): 
		"""Test setup"""
		self.client = app.test_client()
		self.app = app.test_client()

		#Set up the tables in the database
		Base.metadata.create_all(engine)

		#Create folders for test uploads
		os.mkdir(upload_path())
		os.mkdir(upload_photo_path())


	def tearDown(self):
		"""Test teardown"""
		session.close()

		#Remove the tables and their data from the database
		Base.metadata.drop_all(engine)

		#Delete test folders
		shutil.rmtree(upload_path())
		shutil.rmtree(upload_photo_path())	

	def test_join(self):
		#create data for post request
		data = {
			"first_name": "Anne", 
			"last_name": "Jones", 
			"email": "testing@test.com", 
			"password": "password"		
		}	

		response = self.client.post("/api/join", 
				data=json.dumps(data), 
				content_type="application/json", 
				headers=[("Accept", "application/json")]
				)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.mimetype, "application/json")	

		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["user_info"]["first_name"], "Anne")
		self.assertEqual(data["user_info"]["last_name"], "Jones")
		self.assertEqual(data["user_info"]["email"], "testing@test.com")
		self.assertEqual(data["user_info"]["email_confirmed"], 0)

	def test_join_user_exists(self): 
		#create existing user
		user = User(first_name="Test", last_name="Test", email="test@test.com", password="password", conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()

		#create data for post request
		data = {
				"first_name": "Anne", 
				"last_name": "Jones", 
				"email": "test@test.com", 
				"password": "password"		
			}	

		response = self.client.post("/api/join", 
					data=json.dumps(data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")
		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["message"], "User already exists")

	def test_login_user(self): 
		#create user
		user = User(first_name="Test", last_name="Test", email="a@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()

		#create data for post request
		data = {
			"email": "a@test.com",
			"password": "password123"
		}	

		response = self.client.post("/api/login", 
					data=json.dumps(data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["message"], "Successful login")

	def test_login_user_wrong_password(self): 
		#create user
		user = User(first_name="Test", last_name="Test", email="a@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()

		#create data for post request
		data = {
			"email": "a@test.com",
			"password": "password1234"
		}	

		response = self.client.post("/api/login", 
					data=json.dumps(data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["message"], "Invalid email and/or password")	

	def test_get_profile_details(self):
		#create user
		user = User(first_name="John", last_name="Doe", email="john@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()

		#create data for post request to login
		data = {
			"email": "john@test.com",
			"password": "password123"
		}	

		response = self.client.post("/api/login", 
					data=json.dumps(data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)

		#test getting results
		response = self.client.get("/api/profile-details")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["first_name"][0], "John")
		self.assertEqual(data["last_name"][0], "Doe")
		self.assertEqual(data["email"][0], "john@test.com")

	def test_get_pets(self):
		#create user
		user = User(first_name="Jane", last_name="Doe", email="jane@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()
		user_id = session.query(User.id).filter(User.email == "jane@test.com").first()[0]

		#create pets for user
		pet = Pet(name = "Fido", birthdate="2016-05-01", owner_id = user_id)
		session.add(pet)
		session.commit()

		#create data for post request to login
		data = {
			"email": "jane@test.com",
			"password": "password123"
		}	

		response = self.client.post("/api/login", 
					data=json.dumps(data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)
	

		#make request to pet info
		response = self.client.get("/api/pets")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]["name"], "Fido")

	def test_add_pet_post(self):
		#create user
		user = User(first_name="Jane", last_name="Doe", email="jane@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()
		user_id = session.query(User.id).filter(User.email == "jane@test.com").first()[0]

		#create data for post request to login
		login_data = {
			"email": "jane@test.com",
			"password": "password123"
		}	

		response = self.client.post("/api/login", 
					data=json.dumps(login_data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)

		#create data for post request to add pet
		data = {
			"pet-name": "Rufus",
			"pet-birthdate": "2016-05-01"
		}

		response = self.client.post("api/add-pet", 
					data=json.dumps(data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)

		pet = session.query(Pet).filter(Pet.owner_id == user_id).first()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

		self.assertEqual(pet.name, "Rufus")
		self.assertEqual(str(pet.birthdate), "2016-05-01 00:00:00")

	def test_delete_pet(self):
		#create user and pet
		user = User(first_name="Jane", last_name="Doe", email="jane@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()
		user_id = session.query(User.id).filter(User.email == "jane@test.com").first()[0]
		pet = Pet(name="Fido", birthdate="2016-07-01", owner_id=user_id)
		session.add(pet)
		session.commit()
		pet_id = session.query(Pet.id).filter(Pet.name=="Fido").first()[0]

		#create data for post request to login
		login_data = {
			"email": "jane@test.com",
			"password": "password123"
		}	

		response = self.client.post("/api/login", 
					data=json.dumps(login_data), 
					content_type="application/json", 
					headers=[("Accept", "application/json")]
					)
		
		#send request to delete pet
		response = self.client.post("api/delete-pet/" + str(pet_id))

		#check response
		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["message"], "Pet deleted successfully")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

	def test_upload_file_post(self):
		#create user and pet
		user = User(first_name="Jane", last_name="Doe", email="jane@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()
		user_id = session.query(User.id).filter(User.email == "jane@test.com").first()[0]
		pet = Pet(name="Fido", birthdate="2016-07-01", owner_id=user_id)
		session.add(pet)
		session.commit()
		pet_id = session.query(Pet.id).filter(Pet.name=="Fido").first()[0]

		app_client = app.test_client()
		response = app_client.post('api/files', buffered=True,
                           content_type='multipart/form-data',
                           data={'file' : (BytesIO(b'hello there'), 'hello.txt'),
                                 'file-pet-id' : pet_id,
                                 'record-type' : 'Rabies', 
                                 'record-details': 'Rabies Vaccine Certificate' })

		#check response
		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["record_type"], "Rabies")
		self.assertEqual(data["record_details"], "Rabies Vaccine Certificate")

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.mimetype, "application/json")

	def test_delete_file(self):	
		#create user and pet
		user = User(first_name="Jane", last_name="Doe", email="jane@test.com", password=generate_password_hash("password123"), conf_uuid=uuid.uuid4())	
		session.add(user)
		session.commit()
		user_id = session.query(User.id).filter(User.email == "jane@test.com").first()[0]
		pet = Pet(name="Fido", birthdate="2016-07-01", owner_id=user_id)
		session.add(pet)
		session.commit()
		pet_id = session.query(Pet.id).filter(Pet.name=="Fido").first()[0]

		#upload file
		app_client = app.test_client()
		response = app_client.post('api/files', buffered=True,
                           content_type='multipart/form-data',
                           data={'file' : (BytesIO(b'hello there'), 'hello.txt'),
                                 'file-pet-id' : pet_id,
                                 'record-type' : 'Rabies', 
                                 'record-details': 'Rabies Vaccine Certificate' })

		record_id = session.query(Record.id).filter(Record.record_type == "Rabies").first()[0]

		#delete file
		response = self.client.post('api/delete-record-' + str(record_id))

		#check response
		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["message"], "Record deleted successfully")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")



if __name__ == "__main__":
    unittest.main()






