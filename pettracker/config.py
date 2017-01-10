import os

class DevelopmentConfig(object): 
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']#"postgresql://anne:thinkful@localhost:5432/pettracker"
    DEBUG = True
    SECRET_KEY = os.environ.get("PETTRACKER_SECRET_KEY", os.urandom(12))
    UPLOAD_FOLDER = "uploads"
    PHOTO_FOLDER = "photos"

class TestingConfig(object): 
	SQLALCHEMY_DATABASE_URI = "postgresql://anne:thinkful@localhost:5432/pettracker-test"
	DEBUG = False
	SECRET_KEY = "not secret"
	UPLOAD_FOLDER = "uploads-test"
	PHOTO_FOLDER = "photos-test"