from globals import app, timestamp, db
from forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from libs.User import User
import src.crypto as crypto


@app.route("/login", methods=['GET', 'POST'])
def login_route():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = crypto.hash_password(form.password.data)
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            user = User.query.filter_by(email=username, password=password).first()
        if user:
            user.last_login = timestamp()
            login_user(user, remember=form.remember.data, force=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index_route'))
        else:
            flash('Incorrect login!', "danger")
    return render_template("login.html", title="Login Page", form=form, successful=True)


@app.route("/register", methods=['GET', 'POST'])
def register_route():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = crypto.hash_password(form.password.data)
            email = form.email.data
            register_time = timestamp(),
            last_login = register_time
            user = User(
                username=username,
                password=password,
                email=email,
                register_time=register_time,
                last_login=last_login
            )
            db.session.add(user)
            db.session.commit()
            login_user(user, force=True)
            flash('Account created! Please fill additional information.', 'success')
            return redirect(url_for('profile_route', action='edit'))
    return render_template("register.html", title="Register Page", form=form)


@app.route("/logout", methods=['GET'])
@login_required
def logout_route():
    logout_user()
    return render_template("index.html", title="Main Page")
