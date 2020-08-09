from globals import app
from flask import render_template, request


@app.route("/")
@app.route("/index")
def index_route():
    return render_template("index.html")


@app.route("/about", methods=['GET'])
def about_route():
    return render_template("about.html")
