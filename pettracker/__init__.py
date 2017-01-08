import os

from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] ='pettrackermail@gmail.com'
app.config['MAIL_PASSWORD'] = 'iQujA@^7wO61'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

config_path=os.environ.get("CONFIG_PATH", "pettracker.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import api
from . import login