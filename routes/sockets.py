import logging

from globals import db, sessions, socketIO
from src.misc import timestamp, get_rand
from flask_login import current_user
from flask import request, abort
from flask_socketio import emit
from libs.models.Message import Message
from libs.models.Chat import Chat
from libs.models.ChatNotification import ChatNotification
from libs.models.User import User
from libs.models.ChatMember import ChatMember
import json


@socketIO.on('opened')
def handle_new(_):
    if current_user.is_authenticated:
        sessions.update({current_user.id: request.sid})


@socketIO.on('message')
def handle_msg(msg):
    text = msg.get('text')
    # current_user - от кого пришло сообщение
    try:
        user_id = int(msg.get('user_id'))
        chat_id = int(msg.get('chat_id'))
    except TypeError as e:
        logging.error(e)
        return
    # TODO добавить контент
    message = Message(id=get_rand(), chat_id=chat_id, user_id=user_id,
                      time=timestamp(), text=text)
    members = Chat.get_or_404(chat_id).get_members()
    for i in members:
        if i.id != user_id:
            ChatNotification.add(chat_id=chat_id, user_id=i.id)
    db.session.add(message)
    db.session.commit()
    chat = Chat.get_or_404(chat_id)
    if chat is not None and not chat.deleted:
        members = chat.get_members()
        chat.update_last_msg(message)
        for user in members:
            if user.id != user_id:
                session = sessions.get_or_404(user.id)
                if session:
                    emit(
                        'message',
                        json.dumps({
                            'text': text,
                            'message_id': message.id,
                            'username': User.get_or_404(user_id).username,
                            'chat_id': chat_id, 'user_id': user_id
                        }),
                        room=session
                    )
    else:
        abort(404)


@socketIO.on('notify')
def handle_notify(msg):
    type = msg.get('type')
    if type == 'message':
        chat_id = msg.get('chat_id')
        ChatNotification.remove(chat_id=chat_id, user_id=current_user.id)
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
    emit('new_group_chat_ack', 'ack', room=sessions.get_or_404(current_user.id))
