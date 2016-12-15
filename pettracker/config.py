import os

class DevelopmentConfig(object): 
    SQLALCHEMY_DATABASE_URI = "postgresql://anne:thinkful@localhost:5432/pettracker"
    DEBUG = True
    SECRET_KEY = os.environ.get("PETTRACKER_SECRET_KEY", os.urandom(12))