import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

from . import app 

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base, UserMixin): 
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128))
    join_date = Column(DateTime, default=datetime.datetime.now)
    conf_uuid = Column(String(36))
    email_confirmed = Column(Integer, default=0)
    
    pets = relationship("Pet", backref="owner")

    def as_dictionary(self):
        user = {
            "id": self.id, 
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "email": self.email, 
            "password": self.password, 
            "join_date": str(self.join_date),
            "conf_uuid": self.conf_uuid, 
            "email_confirmed": self.email_confirmed
        }
        return user
    
class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    birthdate = Column(DateTime)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    vet_id = Column(Integer, ForeignKey("vets.id"))
    
    appointments = relationship("Appointment", backref="pet")
    vaccines = relationship("Vaccine", backref="pet")
    medications = relationship("Medication", backref="pet")
    food = relationship("Food", uselist=False, backref="pet")
    records = relationship("Record", backref="pet")
    #photos = relationship("Photo", uselist=False, backref="pet")

    def as_dictionary(self): 
        pet = {
            "id": self.id, 
            "name": self.name, 
            "birthdate": str(self.birthdate), 
            "owner_id": self.owner_id, 
            "vet_id": self.vet_id
        }
        return pet
    
class Vet(Base): 
    __tablename__ = "vets"
    
    id = Column(Integer, primary_key=True)
    vet_name = Column(String(128))
    vet_phone = Column(String(15))
    vet_email = Column(String(128))
    
    pets = relationship("Pet", backref="vet")

    def as_dictionary(self):
        vet = {
            "vet_id": self.id,        
            "vet_name": self.vet_name, 
            "vet_phone": self.vet_phone,
            "vet_email": self.vet_email
        }
        return vet
    
class Appointment(Base): 
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True)
    appointment_type = Column(String(128))
    appointment_date = Column(DateTime)
    
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    
class Vaccine(Base):
    __tablename__ = "vaccines"
    
    id = Column(Integer, primary_key=True)
    vaccine_type = Column(String(128), nullable=False)
    administration_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable = False)

    def as_dictionary(self): 
        vaccine = {
            "id": self.id,
            "vaccine_type": self.vaccine_type, 
            "administration_date": str(self.administration_date), 
            "expiration_date": str(self.expiration_date)
        }
        return vaccine
    
class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True)
    medication_name = Column(String(128), nullable=False)
    medication_type = Column(String(128), nullable=False)
    frequency = Column(String(128), nullable=False)
    last_administration_date = Column(DateTime, nullable=False)
    next_administration_date = Column(DateTime, nullable=False)
    
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable = False)
    
class Food(Base):
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True)
    food_name = Column(String(128), nullable=False)
    cups_per_day = Column(Float(8))
    volume_cups = Column(Integer)
    last_purchase_date = Column(DateTime)
    next_purchase_date = Column(DateTime)
    
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable = False)   

    def as_dictionary(self):
        food = {
            "food_name": self.food_name, 
            "cups_per_day": self.cups_per_day
        }
        return food 
    
class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True)
    record_type = Column(String(128))
    record_details = Column(String(1024))
    file_name = Column(String(128), nullable=False)
    file_path = Column(String(128), nullable=False)
    
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable = False)    
    
    def as_dictionary(self): 
        return {
            "id": self.id, 
            "record_type": self.record_type, 
            "record_details": self.record_details, 
            "record_name": self.file_name,
            "path": self.file_path
        }


class Photo(Base): 
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True) 
    file_name = Column(String(128), nullable=False)
    file_path = Column(String(128), nullable=False)

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    def as_dictionary(self):
        return {
            "id": self.id,
            "file_name": self.file_name, 
            "path": self.file_path
        }        

Base.metadata.create_all(engine)    
    

    
    
    
    