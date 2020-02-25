from flask import render_template, url_for, request, redirect, flash
from forms import RegistrationForm, LoginForm, EditProfileForm, NewGroupFrom
from flask_login import login_user, logout_user, current_user, login_required
import libs.crypto as crypto
from libs.ChatRole import ChatRole
from libs.ChatMember import ChatMember
from libs.User import User, set_user_picture
from libs.Group import Group
from libs.Member import Member
from libs.Chat import Chat
from libs.Message import Message
from libs.Friend import Friend
from globals import app, db, socketio, timestamp, get_rand, sessions
from flask_socketio import send, emit
import time, logging
import json


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page", sidebar=True)


@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html", title="About Page", sidebar=True)


# ----------------------------LOGIN-------------------------------------


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
            user.last_login = timestamp()
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
            user = User(username=form.username.data, password=crypto.hash(form.password.data), email=form.email.data, last_login=timestamp())
            db.session.add(user)
            db.session.commit()
            login_user(user, force=True)
            flash('Account created! Please fill additional information.', 'success')
            return redirect(url_for('profile', action='edit'))
    return render_template("register.html", title="Register Page", form=form)


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template("index.html", title="Main Page", sidebar=True)


# -------------------------------------------------------------------------------------------------------------
# ------------------------------------------EDIT PROFILE-------------------------------------------------------

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
            friends = current_user.friends_get()
            return render_template("profile.html", title="Profile", sidebar=True,
                                current_user=current_user, groups=groups, friends=friends, my=True)
        elif action == 'show':
            id = int(request.args.get('id'))
            if not id or id == current_user.id:
                return redirect(url_for("profile", action='my'))
            user = User.get(id)
            groups = user.get_groups()
            friends = user.friends_get()
            chat = ChatMember.get_private_chat(current_user.id, id)
            is_friend = True if current_user in friends else None
            return render_template("profile.html", title="Profile", sidebar=True, chat_id=chat.id if chat else None,
                                current_user=user, groups=groups, friends=friends, is_friend=is_friend)
        elif action == 'edit':
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
        elif action == 'friend_add':
            id = request.args.get('id')
            if not id:
                flash("Somthing went wrong! Please try again.", "error")
                return redirect(request.referrer)
            current_user.friend_add(id)
            flash("Friend added!", "success")
            return redirect(url_for("profile", action='show', id=id))
        elif action == 'friend_remove':
            id = request.args.get('id')
            if not id:
                flash("Somthing went wrong! Please try again.", "error")
                return redirect(request.referrer)
            current_user.friend_remove(id)
            flash("Friend removed!", "success")
            return redirect(url_for("profile", action='show', id=id))

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


# ---------------------------------------------------------------------------------------------------------
# ------------------------------------------GROUPS---------------------------------------------------------


@app.route("/search", methods=['GET'])
@login_required
def search():
    if request.method == 'GET':
        sport = request.args.get('sport')
        groups = Group.get_by_sport(sport)
        return render_template("search.html", query=groups, sidebar=True)
    else:
        return render_template("search.html", sidebar=True)


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    form = NewGroupFrom()
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            return redirect(url_for('group', action='my'))
        elif action == 'new':
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
                new_row = Member(user_id=current_user.id, group_id=group.id, time=timestamp())
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
            new_row = Member(user_id=current_user.id, group_id=group.id, time=timestamp())
            db.session.add(new_row)
            db.session.commit()
            print("Added new group: " + group.name)
            return redirect(url_for('group', action='my'))
        return render_template('new_group.html', form=form, groups=current_user.get_groups(), sidebar=True)


# --------------------------------------------------------------------------------------------------------
# ------------------------------------------SIDEBAR-------------------------------------------------------

@app.route("/myevents", methods=['GET'])
@login_required
def my_events():
    return redirect(url_for('profile'))

@app.route("/mymessages", methods=['GET'])
@login_required
def my_messages():
    return redirect(url_for('profile'))


# --------------------------------------------------------------------------------------------------------
# ------------------------------------------MESSAGES------------------------------------------------------


@app.route("/chat", methods=['GET'])
@login_required
def chat():
    chat_id = request.args.get('chat_id')
    # С кем чат
    user_id = request.args.get('user_id')
    if user_id is None:
        if chat_id is None:
            return redirect(request.referrer)
        chat = Chat.get(int(chat_id))
        members = chat.get_members()
        if len(members) > 2:
            # TODO добавить редирект на групповой чат
            flash("group chat detected", 'error')
            return redirect(request.referrer)
        user_id = members[0].id if members[0].id != current_user.id else members[1].id
        return redirect(url_for("chat", chat_id=chat_id, user_id=user_id))
    else:
        user_id=int(user_id)
    if chat_id is None:
        chat = ChatMember.get_private_chat(current_user.id, int(user_id))
        if chat is None:
            chat = Chat(admin_id=current_user.id, time=timestamp())
            db.session.add(chat)
            db.session.commit()
            chat_id = chat.id
            chat.add_member(current_user.id, is_group=False)
            chat.add_member(int(user_id), is_group=False)
            db.session.commit()
            history=[]
        else:
            return redirect(url_for("chat", chat_id=chat.id, user_id=user_id))
    else:
        history = Chat.get(int(chat_id)).get_history()
        for msg in history:
            msg.is_read = True
        db.session.commit()
        # TODO Написать
        # User.get(int(user_id)).check_messages()

    return render_template("chat.html", user_id=user_id, current_user=current_user, namespace=User.get(user_id).username, chat_id=int(chat_id), messages=history, sidebar=True)


@socketio.on('opened')
def handle_new(msg):
    sessions.update({current_user.id: request.sid})

@socketio.on('message')
def handle_msg(msg):
    text = msg.get('text')
    # от кого пришло сообщение
    user_id = int(msg.get('user_id'))
    chat_id = int(msg.get('chat_id'))
    # TODO добавить контент
    message = Message(id=get_rand(), chat_id=chat_id, user_id=user_id,
                  time=timestamp(), text=text)
    db.session.add(message)
    db.session.commit()
    members = Chat.get(chat_id).get_members()
    for user in members:
        if user.id != user_id:
            emit('message', json.dumps({'text': text, 'username': User.get(user_id).username, 'user_id': user_id}), room=sessions.get(user.id))



if __name__ == "__main__":
    db.create_all()
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    socketio.run(app, debug=True, port=5000)

