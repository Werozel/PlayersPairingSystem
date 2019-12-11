from flask import render_template, url_for, request, redirect, flash, make_response
from forms import RegistrationForm, LoginForm, EditProfileForm
from flask_sqlalchemy import SQLAlchemy
import libs.crypto as crypto
from libs.User import User
from libs.Group import Group
from libs.Users import login as login_user
from globals import app, db, bootstrap


def get_user(cookie) -> User:
    id_s = cookie.get('id')
    current_user = None
    if id_s:
        current_user = User.query.filter_by(id=int(id_s)).first()
    return current_user


@app.route("/")
@app.route("/index")
def index():
    current_user = get_user(request.cookies)
    return render_template("index.html", title="Main Page", sidebar=True, current_user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    current_user = None
    if request.method == 'POST':
        username = form.username.data
        password = crypto.hash(form.password.data)
        current_user = User.query.filter_by(username=username, password=password).first()
        if current_user:
            flash('Logged in!', "success")
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie("id", value=str(current_user.id))
            return resp
        else:
            flash('Incorrect login!', "danger")
    return render_template("login.html", title="Login Page", form=form, successful=True, current_user=current_user)


@app.route("/about")
def about():
    current_user = get_user(request.cookies)
    return render_template("about.html", title="About Page", current_user=current_user)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    current_user = None
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = User(username=form.username.data, password=crypto.hash(form.password.data), email=form.email.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Account created!', 'success')
            resp = make_response(redirect(url_for('edit_profile')))
            resp.set_cookie("id", value=str(current_user.id))
            return resp
    return render_template("register.html", title="Register Page", form=form, current_user=current_user)
 

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    current_user = get_user(request.cookies)
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user:
                current_user.name = form.name.data
                current_user.last_name = form.last_name.data
                current_user.age = form.age.data
                current_user.gender = form.gender.data
                # TODO add image_file link
                db.session.add(current_user)
                db.session.commit()
                flash('Profile edited!', 'success')
                return redirect(url_for('profile'))
    return render_template("edit_profile.html", title="Edit profile", current_user=current_user, form=form)


@app.route("/profile")
def profile():
    current_user = get_user(request.cookies)
    return render_template("profile.html", title="Profile", current_user=current_user, sidebar=True)


@app.route("/log_out", methods=['GET'])
def log_out():
    resp = make_response(render_template("index.html", title="Main Page", sidebar=True, current_user=None))
    resp.set_cookie("id", expires=0) 
    return resp


if __name__ == "__main__":
    print(User.query.all())
    app.run(debug=True)

