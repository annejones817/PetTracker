from flask import render_template

from pettracker import app

@app.route("/")
def index():
    return app.send_static_file("html/index.html")
