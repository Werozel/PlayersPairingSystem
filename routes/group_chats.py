from globals import app, db, timestamp
from flask_login import login_required, current_user
from flask import render_template, request, redirect, flash
from libs.Chat import Chat
from libs.ChatMember import ChatMember
from libs.Group import Group
from libs.ChatNotification import ChatNotification


@app.route("/groupchats", methods=['GET'])
@login_required
def group_chats_route():
    # TODO permissions to show
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
        return render_template(
            "group_chats.html",
            chats=chats,
            group=Group.get(group_id),
            notification=current_user.get_notifications()
        )
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
        ChatNotification.remove(user_id=current_user.id, chat_id=chat_id)
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
