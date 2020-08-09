from globals import db, timestamp, sessions, socketIO, get_rand
from flask_login import current_user
from flask import request
from flask_socketio import emit
from libs.Message import Message
from libs.Chat import Chat
from libs.ChatNotification import ChatNotification
from libs.User import User
from libs.ChatMember import ChatMember
import json


@socketIO.on('opened')
def handle_new(_):
    if current_user.is_authenticated:
        sessions.update({current_user.id: request.sid})


@socketIO.on('message')
def handle_msg(msg):
    text = msg.get('text')
    # current_user - от кого пришло сообщение
    user_id = int(msg.get('user_id'))
    chat_id = int(msg.get('chat_id'))
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
                            'username': User.get_or_404(user_id).username,
                            'chat_id': chat_id, 'user_id': user_id
                        }),
                        room=session
                    )


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
    emit('new_group_chat_ack', 'ack', room=sessions.get(current_user.id))
