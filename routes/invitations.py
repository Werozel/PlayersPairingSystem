from globals import app, db
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash
from libs.Invitation import Invitation
from typing import List


@app.route("/my_invitations", methods=['GET'])
@login_required
def my_invitations_route():
    action = request.args.get('action')
    if not action:
        flash("Something went wrong!", "error")
        return redirect(url_for('my_invitations_route', action='show'))
    elif action == 'show':
        invitations: List[Invitation] = current_user.get_invitations()
        for i in invitations:
            i.read = True
            db.session.add(i)
        db.session.commit()
        return render_template('my_invitations.html', invitations=invitations)
    elif action == 'accept' or action == 'reject':
        invitation_id = int(request.args.get('id'))
        invitation = Invitation.get(invitation_id)
        if current_user.id != invitation.recipient_id:
            flash("No permission!", "error")
        elif action == 'accept':
            invitation.accept()
        else:
            invitation.reject()
        return redirect(url_for("my_invitations_route", action='show'))
    else:
        return redirect(url_for('my_invitations_route', action='show'))