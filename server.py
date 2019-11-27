from flask import Flask, render_template, url_for, request, redirect
from forms import RegistrationForm, LoginForm
from app_config import *


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page", sidebar=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(request.values)
    return render_template("login.html", title="Login Page", form=form, successful=True)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(request.values)
    return render_template("register.html", title="Register Page", form=form)
 



if __name__ == "__main__":
    app.run(debug=True)
