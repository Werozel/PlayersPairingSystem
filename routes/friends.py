from globals import app
from src.misc import get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, abort
from libs.models.User import User


@app.route("/friends", methods=['GET'])
@login_required
def friends_route():
    action = get_arg_or_400('action')
    if action == 'search':
        users = User.query.order_by(User.register_time).all()
        return render_template("show_users.html", current_user=current_user, users=users)
    else:
        abort(400)
