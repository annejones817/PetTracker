import os

class DevelopmentConfig(object): 
    SQL_ALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/pettracker"
    DEBUG = True