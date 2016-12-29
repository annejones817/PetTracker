import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from getpass import getpass
from werkzeug.security import generate_password_hash
from pettracker.database import Base, session, User, Pet, Vet, Appointment, Vaccine, Medication, Food, Record 

from pettracker import app 

manager = Manager(app)

@manager.command
def run(): 
    port=int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)
   

@manager.command
def adduser():
    first_name = input("First Name: ")
    last_name = input("Last Name")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(first_name=first_name, last_name=last_name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()   

class DB(object):
	def __init__(self, metadata): 
		self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)		     

if __name__ == "__main__": 
    manager.run()    