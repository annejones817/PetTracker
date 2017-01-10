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

		print(response)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")

		data = json.loads(response.data.decode("ascii"))
		self.assertEqual(data["first_name"][0], "John")
		self.assertEqual(data["last_name"][0], "Doe")
		self.assertEqual(data["email"][0], "john@test.com")


if __name__ == "__main__":
    unittest.main()






