from globals import app, db, sessions, get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, abort
from forms import EditProfileForm
from libs.User import User
from libs.ChatMember import ChatMember
from libs.Invitation import Invitation, InvitationType
from libs.User import set_user_picture
from flask_socketio import emit
import json


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile_route():
    if request.method == 'GET':
        action = get_arg_or_400('action')
        if action == 'my':
            groups = current_user.get_groups()
            friends = current_user.friends_get()
            return render_template(
                "profile.html",
                title="Profile",
                current_user=current_user,
                user=current_user,
                groups=groups,
                friends=friends,
                my=True
            )
        elif action == 'show':
            id = get_arg_or_400('id', to_int=True)
            user = User.get_or_404(id)
            groups = user.get_groups()
            friends = user.friends_get()
            chat = ChatMember.get_private_chat(current_user.id, id)
            is_friend = True if current_user in friends else None
            return render_template(
                "profile.html",
                title="Profile",
                chat_id=chat.id if chat else None,
                current_user=current_user,
                groups=groups,
                friends=friends,
                is_friend=is_friend,
                user=user
            )
        elif action == 'edit':
            form = EditProfileForm(
                name=current_user.name,
                last_name=current_user.last_name,
                age=current_user.age,
                gender=current_user.gender,
                sport=current_user.sport
            )
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
        elif action == 'friend_add':
            new_friend_id = get_arg_or_400('id', to_int=True)
            invitation_id = Invitation.add(
                InvitationType.FRIEND,
                referrer_id=current_user.id,
                recipient_id=new_friend_id
            )
            if invitation_id != -1:
                emit('invitation', json.dumps({'invitation_id': invitation_id}), room=sessions.get(new_friend_id))
                flash("Invitation sent!", "success")
            else:
                flash("You already sent an invitation to this user!", "info")
            return redirect(url_for("profile_route", action='show', id=new_friend_id))
        elif action == 'friend_remove':
            id = get_arg_or_400('id', to_int=True)
            current_user.friend_remove(id)
            flash("Friend removed!", "success")
            return redirect(url_for("profile_route", action='show', id=id))
        else:
            abort(400)

    elif request.method == 'POST':
        form = EditProfileForm()
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
        else:
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
    else:
        abort(403)
