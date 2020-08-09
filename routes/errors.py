from globals import app
from flask import render_template


@app.errorhandler(400)
def bad_request(_):
    return render_template("400.html"), 400


@app.errorhandler(403)
def forbidden(_):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(_):
    return render_template("500.html"), 500
