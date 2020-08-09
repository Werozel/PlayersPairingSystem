from globals import app, db, timestamp, get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, abort
from libs.Chat import Chat
from libs.ChatMember import ChatMember
from libs.User import User
from libs.ChatNotification import ChatNotification


# TODO Rewrite this
@app.route("/chats", methods=['GET'])
@login_required
def chats_route():
    action = get_arg_or_400('action')

    if action == 'show':
        chat_id = get_arg_or_400('chat_id', to_int=True)
        user_id = get_arg_or_400('user_id', to_int=True)    # С кем чат
        if user_id is None:
            if chat_id is None:
                return redirect(url_for('chat', action='all'))
            chat = Chat.get_or_404(chat_id)
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
        if chat_id is None:
            chat = ChatMember.get_private_chat(current_user.id, user_id)
            if chat is None:
                chat = Chat(admin_id=current_user.id, time=timestamp())
                db.session.add(chat)
                db.session.commit()
                chat_id = chat.id
                chat.add_member(current_user.id, is_group=False)
                chat.add_member(user_id, is_group=False)
                db.session.commit()
                history = []
            elif chat.deleted is not None:
                return redirect(url_for('chats_route', action='all'))
            else:
                return redirect(url_for("chats_route", action='show', chat_id=chat.id, user_id=user_id))
        else:
            history = Chat.get_or_404(int(chat_id)).get_history()
            ChatNotification.remove(user_id=current_user.id, chat_id=chat_id)

        return render_template(
            "chat.html",
            user_id=user_id,
            current_user=current_user,
            chat_name=User.get_or_404(user_id).username,
            chat=Chat.get_or_404(chat_id),
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
        chat_id = get_arg_or_400('chat_id', to_int=True)
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
        abort(400)
