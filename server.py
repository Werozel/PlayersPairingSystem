from flask import render_template, url_for, request, redirect, flash, make_response
from forms import RegistrationForm, LoginForm, EditProfileForm
from flask_login import login_user, logout_user, current_user
import libs.crypto as crypto
from libs.User import User
from globals import app, db


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
            login_user(user, remember=form.remember.data)
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
        if form.validate_on_submit():
            user = User(username=form.username.data, password=crypto.hash(form.password.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Now you can login.', 'success')
            return redirect(url_for('login'))
    return render_template("register.html", title="Register Page", form=form)
 

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.last_name = form.last_name.data
            current_user.age = form.age.data
            current_user.gender = form.gender.data
            # TODO add image_file link
            db.session.add(current_user)
            db.session.commit()
            flash('Profile edited!', 'success')
            return redirect(url_for('profile'))
    return render_template("edit_profile.html", title="Edit profile", form=form)


@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile", sidebar=True, current_user=current_user)


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return render_template("index.html", title="Main Page", sidebar=True)


if __name__ == "__main__":
    app.run(debug=True)

