from flask import render_template, url_for, request, redirect, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import libs.crypto as crypto
from libs.User import User
from libs.Group import Group
from libs.Users import login as login_user
from globals import app, db

current_user = None

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page", sidebar=True, current_user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global current_user
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = crypto.hash(form.password.data)
        current_user = User.query.filter_by(username=username, password=password).first()
        if current_user:
            flash('Logged in!', "success")
            return redirect(url_for('index'))
        else:
            flash('Incorrect login!', "danger")
    return render_template("login.html", title="Login Page", form=form, successful=True, current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/register", methods=['GET', 'POST'])
def register():
    global current_user
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = User(username=form.username.data, password=crypto.hash(form.password.data), email=form.email.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Account created!', 'success')
            return redirect(url_for('edit_profile'))
    return render_template("register.html", title="Register Page", form=form, current_user=current_user)
 

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    return render_template("edit_profile.html", title="Edit profile", current_user=current_user)


@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile", current_user=current_user, sidebar=True)


@app.route("/log_out", methods=['GET'])
def log_out():
    global current_user
    current_user = None
    return render_template("index.html", title="Main Page", sidebar=True, current_user=current_user)


if __name__ == "__main__":
    print(User.query.all())
    app.run(debug=True)

