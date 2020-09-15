from globals import app, db
from src.misc import timestamp, get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, abort
from flask_babel import gettext
from forms import NewGroupFrom
from libs.models.Group import Group
from libs.models.GroupMember import GroupMember
from libs.models.Invitation import InvitationType, Invitation


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group_route():

    if request.method == 'GET':
        action = get_arg_or_400('action')

        if not action:
            flash(gettext("Something went wrong!"), "error")
            return redirect(url_for('group_route', action='my'))

        elif action == 'my':
            return render_template('my_groups.html', groups=current_user.get_groups())

        elif action == 'new':
            new_group_form = NewGroupFrom()
            return render_template('new_group.html', form=new_group_form, groups=current_user.get_groups())

        group_id = get_arg_or_400('id', to_int=True)
        group = Group.get_or_404(group_id)
        members = group.get_members()
        is_member = current_user in members
        events = group.get_events()
        is_group_admin = group.admin_id == current_user.id
        if not is_member:
            is_member = None

        if action == 'delete' and is_group_admin:
            group.delete()
            return redirect(url_for('group_route', action='my'))

        elif action == 'edit' and is_group_admin:
            edit_group_form = NewGroupFrom(
                closed=group.closed,
                name=group.name,
                sport=group.sport
            )
            return render_template('edit_group.html', form=edit_group_form, group=group)

        elif action == 'show':
            return render_template(
                'group.html',
                group=group,
                members=members,
                is_member=is_member,
                events=events,
                is_group_admin=is_group_admin
            )

        elif action == 'join':
            if current_user not in members:
                if group.closed:
                    Invitation.add(type=InvitationType.TO_GROUP, recipient_id=group.id, referrer_id=current_user.id)
                    flash(gettext("Invitation sent!"), "success")
                else:
                    new_row = GroupMember(user_id=current_user.id, group_id=group.id, time=timestamp())
                    db.session.add(new_row)
                    db.session.commit()
                    members.append(current_user)
                    is_member = True
            return render_template(
                'group.html',
                group=group,
                members=members,
                is_member=is_member,
                events=events,
                is_group_admin=is_group_admin
            )

        elif action == 'leave':
            if current_user in members:
                row = GroupMember.query.filter_by(user_id=current_user.id, group_id=group.id).first()
                db.session.delete(row)
                db.session.commit()
                members.remove(current_user)
                is_member = None
            return render_template(
                'group.html',
                group=group,
                members=members,
                is_member=is_member,
                events=events,
                is_admin=is_group_admin
            )
        else:
            abort(403)

    else:
        type = get_arg_or_400('type')

        if type == 'edit':
            group_id = get_arg_or_400('id', to_int=True)
            group = Group.get_or_404(group_id)

            edit_group_form = NewGroupFrom(current_group=group)
            if edit_group_form.validate_on_submit():
                group.closed = edit_group_form.closed.data
                group.name = edit_group_form.name.data
                group.sport = edit_group_form.sport.data
                db.session.add(group)
                db.session.commit()
                return redirect(url_for('group_route', action='show', id=group_id))
            else:
                return render_template('edit_group.html', form=edit_group_form, group=group)

        elif type == 'new':
            new_group_form = NewGroupFrom()
            if new_group_form.validate_on_submit():
                group = Group(
                    admin_id=current_user.id,
                    name=new_group_form.name.data,
                    sport=new_group_form.sport.data,
                    closed=new_group_form.closed.data
                )
                db.session.add(group)
                db.session.commit()
                new_row = GroupMember(user_id=current_user.id, group_id=group.id, time=timestamp())
                db.session.add(new_row)
                db.session.commit()
                return redirect(url_for('group_route', action='show', id=group.id))
            else:
                return render_template('new_group.html', form=new_group_form, groups=current_user.get_groups())

        else:
            abort(400)
