from globals import app
from flask_login import login_required, current_user
from flask import render_template, request, redirect
from libs.User import User


@app.route("/friends", methods=['GET'])
@login_required
def friends_route():
    action = request.args.get('action')
    if action == 'search':
        users = User.query.order_by(User.register_time).all()
        return render_template("show_users.html", current_user=current_user, users=users)
    else:
        return redirect(request.referrer)
