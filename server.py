from flask import render_template, url_for, request, redirect, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import libs.crypto as crypto
from libs.User import User
from libs.Group import Group
from libs.Users import login as login_user
from globals import app, db



@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page", sidebar=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print(request.values)
        """if form.username.data == 'admin' and form.password.data == 'admin':
            flash('Logged in!', "success")
            return redirect(url_for('index'))"""
        username = form.username.data
        password = crypto.hash(form.password.data)
        current_user = login_user(username, password)
        if current_user:
            flash('Logged in!', "success")
            return redirect(url_for('index'))
        else:
            flash('Incorrect login!', "danger")
    return render_template("login.html", title="Login Page", form=form, successful=True)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print(request.values)
        if form.validate_on_submit():
            flash('Account created!', 'success')
            return redirect(url_for('edit_profile'))
    return render_template("register.html", title="Register Page", form=form)
 

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    return render_template("edit_profile.html", title="Edit profile")


@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")


if __name__ == "__main__":
    app.run(debug=True)

