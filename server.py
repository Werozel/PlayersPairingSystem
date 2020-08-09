from globals import app, db, socketIO
import logging
import constants.app_config as app_config
# necessary imports to register routes
import routes.chats
import routes.events
import routes.friends
import routes.group_chats
import routes.groups
import routes.index
import routes.invitations
import routes.login
import routes.profile
import routes.search
import routes.sockets
import routes.errors


if __name__ == "__main__":
    db.create_all()

    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    socketIO.run(app, debug=app_config.DEBUG, port=5000, host='0.0.0.0')
