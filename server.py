from flask import render_template, url_for, request, redirect, flash, make_response
from forms import RegistrationForm, LoginForm, EditProfileForm, NewGroupFrom
from flask_login import login_user, logout_user, current_user, login_required
import libs.crypto as crypto
from libs.User import User, set_user_picture
from libs.Group import Group
from libs.Member import Member
from globals import app, db


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page", sidebar=True)


@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html", title="About Page", sidebar=True)


#----------------------------LOGIN-------------------------------------


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


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template("index.html", title="Main Page", sidebar=True)


#-------------------------------------------------------------------------------------------------------------
#------------------------------------------EDIT PROFILE-------------------------------------------------------

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            action = 'my'
        if action == 'my':
            groups = current_user.get_groups()
            return render_template("profile.html", title="Profile", sidebar=True,
                                current_user=current_user, groups=groups)
        elif action == 'show':
            id = request.args.get('id')
            if not id:
                id = current_user.id
            user = User.get(id)
            groups = user.get_groups()
            return render_template("profile.html", title="Profile", sidebar=True,
                                current_user=user, groups=groups)
        elif action == 'edit':
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
    else:
        if form.validate_on_submit():
            if form.picture.data:
                set_user_picture(form.picture.data)
            current_user.name = form.name.data
            current_user.last_name = form.last_name.data
            current_user.age = form.age.data
            current_user.gender = form.gender.data
            if len(form.sport.data):
                current_user.sport = form.sport.data
            db.session.add(current_user)
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('profile'))
        return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)


#---------------------------------------------------------------------------------------------------------
#------------------------------------------GROUPS---------------------------------------------------------


@app.route("/search", methods=['GET'])
@login_required
def search():
    sport = request.args.get('sport')
    groups = Group.get_by_sport(sport)
    return render_template("search.html", query=groups, sidebar=True)


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    form = NewGroupFrom()
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            flash("Invalid request!", 'warning')
            return redirect(url_for('group', action='my'))
        if action == 'new':
            return render_template('new_group.html', form=form, groups=current_user.get_groups(), sidebar=True)
        elif action == 'my':
            return render_template('my_groups.html', groups=current_user.get_groups(), sidebar=True)

        id = int(request.args.get('id'))
        group = Group.get(id)
        members = group.get_members()
        is_member = current_user in members
        if not is_member:
            is_member = None
        if action == 'show':
            pass
        elif action == 'join':
            if current_user not in members:
                new_row = Member(user_id=current_user.id, group_id=group.id)
                db.session.add(new_row)
                db.session.commit()
                members.append(current_user)
                is_member = True
        elif action == 'leave':
            if current_user in members:
                row = Member.query.filter_by(user_id=current_user.id, group_id=group.id).first()
                db.session.delete(row)
                db.session.commit()
                members.remove(current_user)
                is_member = None
        return render_template('group.html', group=group, members=members, sidebar=True, is_member=is_member)
    else:
        if form.validate_on_submit():
            group = Group(admin_id=current_user.id, name=form.name.data, sport=form.sport.data)
            db.session.add(group)
            db.session.commit()
            new_row = Member(user_id=current_user.id, group_id=group.id)
            db.session.add(new_row)
            db.session.commit()
            print("Added new group: " + group.name)
            return redirect(url_for('group', action='my'))
        return render_template('new_group.html', form=form, groups=current_user.get_groups(), sidebar=True)
#--------------------------------------------------------------------------------------------------------
#------------------------------------------SIDEBAR-------------------------------------------------------

@app.route("/myevents", methods=['GET'])
@login_required
def my_events():
    return redirect(url_for('profile'))

@app.route("/mymessages", methods=['GET'])
@login_required
def my_messages():
    return redirect(url_for('profile'))



if __name__ == "__main__":
    app.run(debug=True)

