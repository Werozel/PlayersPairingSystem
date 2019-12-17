from flask import render_template, url_for, request, redirect, flash, make_response
from forms import RegistrationForm, LoginForm, EditProfileForm
from flask_login import login_user, logout_user, current_user, login_required
import libs.crypto as crypto
from libs.User import User
from globals import app, db
import secrets
import os


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page", sidebar=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = crypto.hash(form.password.data)
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            user = User.query.filter_by(email=username, password=password).first()
        if user:
            login_user(user, remember=form.remember.data, force=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Incorrect login!', "danger")
    return render_template("login.html", title="Login Page", form=form, successful=True)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page", sidebar=True)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, password=crypto.hash(form.password.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, force=True)
            flash('Account created! Please fill additional information.', 'success')
            return redirect(url_for('edit_profile'))
    return render_template("register.html", title="Register Page", form=form)
 

def set_user_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    picture.save(picture_path)
    current_user.image_file = picture_fn


@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.picture.data:
                set_user_picture(form.picture.data)
            current_user.name = form.name.data
            current_user.last_name = form.last_name.data
            current_user.age = form.age.data
            current_user.gender = form.gender.data
            db.session.add(current_user)
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('profile'))
    return render_template("edit_profile.html", title="Edit profile", form=form)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile", sidebar=True,
                           current_user=current_user)


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template("index.html", title="Main Page", sidebar=True)


if __name__ == "__main__":
    app.run(debug=True)

