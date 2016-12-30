import os.path

from pettracker import app

def upload_path(filename=""):
    return os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)

def upload_photo_path(filename=""): 
	return os.path.join(app.root_path, app.config["PHOTO_FOLDER"], filename)    