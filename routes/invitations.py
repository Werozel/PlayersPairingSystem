from globals import app, db, get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, abort
from libs.Invitation import Invitation
from typing import List


@app.route("/my_invitations", methods=['GET'])
@login_required
def my_invitations_route():
    action = get_arg_or_400('action')
    if action == 'show':
        invitations: List[Invitation] = current_user.get_invitations()
        for i in invitations:
            i.read = True
            db.session.add(i)
        db.session.commit()
        return render_template('my_invitations.html', invitations=invitations)
    elif action == 'accept' or action == 'reject':
        invitation_id = get_arg_or_400('id', to_int=True)
        invitation = Invitation.get_or_404(invitation_id)
        if current_user.id != invitation.recipient_id:
            abort(403)
        elif action == 'accept':
            invitation.accept()
        else:
            invitation.reject()
        return redirect(url_for("my_invitations_route", action='show'))
    else:
        abort(400)
