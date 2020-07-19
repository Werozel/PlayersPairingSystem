from flask import render_template, url_for, request, redirect, flash
from forms import RegistrationForm, LoginForm, EditProfileForm, NewGroupFrom, SearchGroupForm, NewEventForm
from flask_login import login_user, logout_user, current_user, login_required
import libs.crypto as crypto
from libs.ChatRole import ChatRole
from libs.Friend import Friend
from libs.ChatMember import ChatMember
from libs.User import User, set_user_picture
from libs.Group import Group
from libs.GroupMember import GroupMember
from libs.Chat import Chat
from libs.Notification import Notification
from libs.Message import Message
from libs.Event import Event
from libs.EventMember import EventMember
from globals import app, db, socketIO, timestamp, get_rand, sessions
from flask_socketio import emit
import logging
import json


@app.route("/")
@app.route("/index")
def index_route():
    return render_template("index.html")


@app.route("/about", methods=['GET'])
def about_route():
    return render_template("about.html")


# ----------------------------LOGIN-------------------------------------


@app.route("/login", methods=['GET', 'POST'])
def login_route():
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
            return redirect(next_page) if next_page else redirect(url_for('index_route'))
        else:
            flash('Incorrect login!', "danger")
    return render_template("login.html", title="Login Page", form=form, successful=True)


@app.route("/register", methods=['GET', 'POST'])
def register_route():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, password=crypto.hash(form.password.data), email=form.email.data,
                        register_time=timestamp(), last_login=timestamp())
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


# -------------------------------------------------------------------------------------------------------------
# ------------------------------------------EDIT PROFILE-------------------------------------------------------

@app.route("/search_group", methods=['GET', 'POST'])
@login_required
def search_group_route():
    search_group_form = SearchGroupForm()
    if request.method == 'GET':
        sport = request.args.get('sport')
        if sport is None:
            groups = Group.query.limit(30).all()
        else:
            groups = Group.get_by_sport(sport)
        return render_template("search_group.html", query=groups, form=search_group_form)
    elif request.method == 'POST':
        name = search_group_form.name.data
        sport = search_group_form.sport.data
        groups = Group.query.filter(Group.name.ilike(f"%{name}%")).\
            filter(Group.sport == sport if sport != "None" else Group.sport == Group.sport).all()
        return render_template("search_group.html", query=groups, form=search_group_form)
    else:
        groups = Group.query.limit(50).all()
        return render_template("search_group.html", query=groups, form=search_group_form)


# ---------------------------------------------------------------------------------------------------------
# ------------------------------------------GROUPS---------------------------------------------------------


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile_route():
    form = EditProfileForm()
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            action = 'my'
        if action == 'my':
            groups = current_user.get_groups()
            friends = current_user.friends_get()
            return render_template("profile.html", title="Profile", current_user=current_user,
                                   user=current_user, groups=groups, friends=friends, my=True)
        elif action == 'show':
            id = int(request.args.get('id'))
            if not id or id == current_user.id:
                return redirect(url_for("profile_route", action='my'))
            user = User.get(id)
            groups = user.get_groups()
            friends = user.friends_get()
            chat = ChatMember.get_private_chat(current_user.id, id)
            is_friend = True if current_user in friends else None
            return render_template("profile.html", title="Profile", chat_id=chat.id if chat else None,
                                   current_user=current_user, groups=groups, friends=friends, is_friend=is_friend,
                                   user=user)
        elif action == 'edit':
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
        elif action == 'friend_add':
            id = request.args.get('id')
            if not id:
                flash("Something went wrong! Please try again.", "error")
                return redirect(request.referrer)
            current_user.friend_add(id)
            flash("Friend added!", "success")
            return redirect(url_for("profile_route", action='show', id=id))
        elif action == 'friend_remove':
            id = request.args.get('id')
            if not id:
                flash("Something went wrong! Please try again.", "error")
                return redirect(request.referrer)
            current_user.friend_remove(id)
            flash("Friend removed!", "success")
            return redirect(url_for("profile_route", action='show', id=id))

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
            return redirect(url_for('profile_route'))
        return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group_route():
    form = NewGroupFrom()
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            return redirect(url_for('group_route', action='my'))
        elif action == 'new':
            return render_template('new_group.html', form=form, groups=current_user.get_groups())
        elif action == 'my':
            return render_template('my_groups.html', groups=current_user.get_groups())

        id = int(request.args.get('id'))
        group = Group.get(id)
        members = group.get_members()
        is_member = current_user in members
        events = group.get_events()
        print(f"events = {events}")
        if not is_member:
            is_member = None
        if action == 'show':
            pass
        elif action == 'join':
            if current_user not in members:
                new_row = GroupMember(user_id=current_user.id, group_id=group.id, time=timestamp())
                db.session.add(new_row)
                db.session.commit()
                members.append(current_user)
                is_member = True
        elif action == 'leave':
            if current_user in members:
                row = GroupMember.query.filter_by(user_id=current_user.id, group_id=group.id).first()
                db.session.delete(row)
                db.session.commit()
                members.remove(current_user)
                is_member = None
        return render_template('group.html', group=group, members=members, is_member=is_member, events=events)
    else:
        if form.validate_on_submit():
            group = Group(admin_id=current_user.id, name=form.name.data, sport=form.sport.data)
            db.session.add(group)
            db.session.commit()
            new_row = GroupMember(user_id=current_user.id, group_id=group.id, time=timestamp())
            db.session.add(new_row)
            db.session.commit()
            return redirect(url_for('group_route', action='my'))
        return render_template('new_group.html', form=form, groups=current_user.get_groups())


# --------------------------------------------------------------------------------------------------------
# ------------------------------------------ EVENTS ------------------------------------------------------

@app.route("/event", methods=['GET', 'POST'])
@login_required
def event_route():
    new_event_form = NewEventForm(groups=current_user.get_groups())

    def args_error():
        flash("Invalid request", 'error')
        return redirect(url_for(request.referrer))

    action = request.args.get('action')
    if request.method == 'GET':
        if action == "my":
            events = current_user.get_events()
            return render_template(
                "my_events.html",
                events=events if len(events) > 0 else None,
                current_user=current_user
            )
        elif action == "show":
            try:
                event_id = int(request.args.get('id'))
            except ValueError:
                return args_error()
            event = Event.get(event_id)
            if event is None:
                return args_error()
            group = event.group
            group = group if group else None
            members = event.get_members()
            is_member = True if current_user in members else None
            members = members if len(members) > 0 else None
            return render_template("event.html", event=event, group=group, members=members, is_member=is_member)
        elif action == "join" or action == "leave":
            try:
                event_id = int(request.args.get('id'))
            except ValueError:
                return args_error()
            event = Event.get(event_id)
            if event is None:
                return args_error()
            if action == "join":
                event.add_member(current_user)
            else:
                event.remove_member(current_user)
            return redirect(url_for('event_route', action='show', id=event_id))
        elif action == "new":
            return render_template("new_event.html", form=new_event_form)
        elif action == "find_people":
            try:
                event_id = int(request.args.get('id'))
            except Exception:
                return args_error()
            event = Event.get(event_id)
            # FIXME сделать нормальный фильтр
            event_users = set(event.get_members())
            all_users = set(User.query.order_by(User.register_time).all())
            users: list = list(filter(lambda user_tmp: event.sport in user_tmp.sport, list(all_users - event_users)))
            return render_template("find_people.html", event_id=event.id, people=users if len(users) > 0 else None)
        elif action == "add_user":
            try:
                user_id = int(request.args.get('user_id'))
                event_id = int(request.args.get('event_id'))
            except ValueError:
                return args_error()
            user = User.get(user_id)
            event = Event.get(event_id)
            event.add_member(user)
            # TODO делать не редирект, а изменение кнопки
            return redirect(url_for('event_route', action='find_people', id=event_id))
        else:
            return args_error()
    else:
        if new_event_form.validate_on_submit():
            name = new_event_form.name.data
            description = new_event_form.description.data
            sport = new_event_form.sport.data
            group_id = new_event_form.assigned_group.data
            group_id = None if group_id == "None" else int(group_id)
            time = new_event_form.time.data
            new_event = Event(name=name, description=description, sport=sport, group_id=group_id,
                              creation_time=timestamp(), creator=current_user.id, time=time)
            db.session.add(new_event)
            db.session.commit()
            new_event_member = EventMember(event_id=new_event.id, user_id=current_user.id, time=timestamp())
            db.session.add(new_event_member)
            db.session.commit()
            return redirect(url_for('event_route', action='my'))
        else:
            return redirect(request.url)


@app.route("/friends", methods=['GET'])
@login_required
def friends_route():
    action = request.args.get('action')
    if action == 'search':
        users = User.query.order_by(User.register_time).all()
        return render_template("show_users.html", current_user=current_user, users=users)
    else:
        return redirect(request.referrer)


# --------------------------------------------------------------------------------------------------------
# ------------------------------------------MESSAGES------------------------------------------------------

@app.route("/groupchats", methods=['GET'])
@login_required
def group_chats_route():

    def args_error():
        flash('Invalid request! Try updating the page.', 'error')
        return redirect(request.referrer)

    action = request.args.get('action')
    if action == 'all':
        group_id = request.args.get('id')
        if group_id is None:
            return args_error()
        group_id = int(group_id)
        chats = Chat.query.filter_by(group_id=group_id, deleted=None).all()
        return render_template("group_chats.html",
                               chats=chats, group=Group.get(group_id),
                               notification=current_user.get_notifications())
    elif action == 'delete':
        chat_id = request.args.get('chat_id')
        if chat_id is None:
            return args_error()
        else:
            chat_id = int(chat_id)
        chat = Chat.get(chat_id)
        chat.deleted = timestamp()
        members = ChatMember.query.filter_by(chat_id=chat_id).all()
        for member in members:
            member.deleted = timestamp()
        db.session.commit()
        return redirect(request.referrer)
    elif action == 'show':
        try:
            chat_id = int(request.args.get('chat_id'))
        except ValueError:
            return args_error()
        chat = Chat.get(chat_id)
        group = Group.get(chat.group_id)
        chat.add_member(id=current_user.id)
        Notification.remove(user_id=current_user.id, chat_id=chat_id)
        return render_template(
            "chat.html",
            group=group,
            chat=chat,
            current_user=current_user,
            messages=chat.get_history()
        )
    elif action == 'add_members':
        return redirect(request.referrer)
    else:
        return args_error()


@app.route("/chats", methods=['GET'])
@login_required
def chats_route():
    action = request.args.get('action')
    if action == 'show':
        chat_id = request.args.get('chat_id')
        # С кем чат
        user_id = request.args.get('user_id')
        if user_id is None:
            if chat_id is None:
                return redirect(url_for('chat', action='all'))
            chat = Chat.get(int(chat_id))
            if chat.deleted is not None:
                redirect(url_for('chats_route', action='all'))
            members = chat.get_members()
            if len(members) > 2:
                return redirect(url_for('group_chats_route', action='show', chat_id=chat_id))
            elif len(members) < 2:
                user_id = 'Deleted'
            else:
                user_id = members[0].id if members[0].id != current_user.id else members[1].id
            return redirect(url_for("chats_route", action='show', chat_id=chat_id, user_id=user_id))
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
                history = []
            elif chat.deleted is not None:
                return redirect(url_for('chats_route', action='all'))
            else:
                return redirect(url_for("chats_route", action='show', chat_id=chat.id, user_id=user_id))
        else:
            history = Chat.get(int(chat_id)).get_history()
            Notification.remove(user_id=current_user.id, chat_id=int(chat_id))

        return render_template(
            "chat.html",
            user_id=user_id,
            current_user=current_user,
            chat_name=User.get(user_id).username,
            chat=Chat.get(int(chat_id)),
            messages=history
        )
    elif action == 'all':
        chats = ChatMember.get_user_chats(current_user.id)
        for i in chats:
            if i.name is None:
                members = i.get_members()
                for u in members:
                    if u.id != current_user.id:
                        i.name = u.username
        return render_template(
            "my_chats.html",
            notifications=current_user.get_notifications(),
            current_user=current_user,
            chats=chats
        )
    elif action == 'delete':
        chat_id = request.args.get('chat_id')
        if chat_id is None:
            return redirect(url_for('chats_route', action='all'))
        chat_id = int(chat_id)
        chat_member = ChatMember.query.filter_by(chat_id=chat_id, user_id=current_user.id).first()
        if chat_member is None:
            return redirect(request.referrer)
        chat_member.deleted = timestamp()
        db.session.commit()
        if chat_member.is_group:
            return redirect(request.referrer)
        return redirect(url_for('chats_route', action='all'))
    else:
        return redirect(url_for('chats_route', action='all'))


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------- SocketIO -------------------------------------------------


@socketIO.on('opened')
def handle_new(_):
    if current_user.is_authenticated:
        sessions.update({current_user.id: request.sid})


@socketIO.on('message')
def handle_msg(msg):
    text = msg.get('text')
    # current_user - тоже от кого пришло сообщение
    user_id = int(msg.get('user_id'))
    chat_id = int(msg.get('chat_id'))
    # TODO добавить контент
    message = Message(id=get_rand(), chat_id=chat_id, user_id=user_id,
                      time=timestamp(), text=text)
    members = Chat.get(chat_id).get_members()
    for i in members:
        if i.id != user_id:
            Notification.add(chat_id=chat_id, user_id=i.id)
    db.session.add(message)
    db.session.commit()
    chat = Chat.get(chat_id)
    if chat is not None and chat.deleted is None:
        members = chat.get_members()
        chat.update_last_msg(message)
        for user in members:
            if user.id != user_id:
                session = sessions.get(user.id)
                if session:
                    emit(
                        'message',
                        json.dumps({
                            'text': text,
                            'message_id': message.id,
                            'username': User.get(user_id).username,
                            'chat_id': chat_id, 'user_id': user_id
                        }),
                        room=session
                    )


@socketIO.on('notify')
def handle_notify(msg):
    type = msg.get('type')
    if type == 'message':
        chat_id = msg.get('chat_id')
        Notification.remove(chat_id=chat_id, user_id=current_user.id)
        db.session.commit()
    else:
        pass


@socketIO.on('new_group_chat')
def handle_new_group_chat(msg):
    name = msg.get('name')
    group_id = int(msg.get('group_id'))
    chat = Chat(name=name, admin_id=current_user.id, time=timestamp(), group_id=group_id)
    db.session.add(chat)
    db.session.commit()
    chat_member = ChatMember(user_id=current_user.id, chat_id=chat.id, is_group=True)
    db.session.add(chat_member)
    db.session.commit()
    emit('new_group_chat_ack', 'ack')


if __name__ == "__main__":
    db.create_all()

    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    socketIO.run(app, debug=True, port=5000, host='0.0.0.0')
