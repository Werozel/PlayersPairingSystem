from globals import app, db
from src.misc import timestamp, get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, request, redirect, abort
from libs.models.Chat import Chat
from libs.models.ChatMember import ChatMember
from libs.models.Group import Group
from libs.models.ChatNotification import ChatNotification


@app.route("/groupchats", methods=['GET'])
@login_required
def group_chats_route():
    # TODO permissions to show

    action = get_arg_or_400('action')
    if action == 'all':
        group_id = get_arg_or_400('id', to_int=True)
        chats = Chat.query.filter_by(group_id=group_id, deleted=None).all()
        return render_template(
            "group_chats.html",
            chats=chats,
            group=Group.get_or_404(group_id),
            notification=current_user.get_notifications()
        )

    chat_id = get_arg_or_400('chat_id', to_int=True)
    chat = Chat.get_or_404(chat_id)

    if action == 'delete':
        chat.deleted = timestamp()
        members = ChatMember.query.filter_by(chat_id=chat_id).all()
        for member in members:
            member.deleted = timestamp()
        db.session.commit()
        return redirect(request.referrer)

    elif action == 'show':
        group = Group.get_or_404(chat.group_id)
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
        abort(400)
    else:
        abort(400)
