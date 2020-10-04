from globals import app, db
from src.misc import timestamp, get_arg_or_none, get_cookie
from forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, request, flash, abort
from flask_babel import gettext
from flask_login import login_user, login_required, logout_user
from libs.models.User import User
import src.crypto as crypto


@app.route("/login", methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        form = LoginForm()
        return render_template("login.html", title="Login Page", form=form, successful=True)
    elif request.method == 'POST':
        form = LoginForm()
        username = form.username.data
        password = crypto.hash_password(form.password.data)
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            user.last_login = timestamp()
            user.last_login_ip = request.remote_addr
            user.language = get_cookie('language', user.language)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember.data, force=True)
            next_page = get_arg_or_none('next')
            return redirect(next_page) if next_page else redirect(url_for('index_route'))
        else:
            flash(gettext("Incorrect login!"), "danger")
            return render_template("login.html", title="Login Page", form=form, successful=True)

    else:
        abort(403)


@app.route("/register", methods=['GET', 'POST'])
def register_route():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template("register.html", title="Register Page", form=form)
    elif request.method == 'POST':
        form = RegistrationForm()
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
                last_login=last_login,
                last_login_ip=request.remote_addr,
                city=form.city.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user, force=True)
            flash(gettext('Account created! Please fill additional information.'), 'success')
            return redirect(url_for('profile_route', action='edit'))
        else:
            return render_template("register.html", title="Register Page", form=form)
    else:
        abort(403)


@app.route("/logout", methods=['GET'])
@login_required
def logout_route():
    logout_user()
    return redirect(url_for('index_route'))
