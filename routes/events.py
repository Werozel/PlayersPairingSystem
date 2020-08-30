from globals import app, db
from src.misc import timestamp, get_arg_or_400
from flask_login import login_required, current_user
from flask_babel import gettext
from flask import render_template, request, redirect, url_for, flash, abort
from forms import NewEventForm, EditEventForm
from libs.models.Event import Event
from libs.models.EventMember import EventMember
from libs.models.Group import Group
from libs.models.User import User
from libs.models.Invitation import Invitation, InvitationType


@app.route("/event", methods=['GET', 'POST'])
@login_required
def event_route():
    if request.method == 'GET':

        action = get_arg_or_400('action')
        if action == 'my':
            events = current_user.get_events()
            return render_template(
                "my_events.html",
                events=events if len(events) > 0 else None
            )

        elif action == 'new':
            new_event_form = NewEventForm(groups=current_user.get_groups())
            return render_template("new_event.html", form=new_event_form)

        event_id = get_arg_or_400('id', to_int=True)
        event = Event.get_or_404(event_id)

        if action == 'delete':
            event.delete()
            return redirect(url_for("event_route", action='my'))

        elif action == 'edit':
            edit_event_form = EditEventForm(
                closed=event.closed,
                name=event.name,
                description=event.description,
                sport=event.sport,
                time=event.time
            )
            return render_template("edit_event.html", form=edit_event_form, event=event)

        elif action == 'show':
            group = event.group
            group: Group = group if group else None
            members = event.get_members()
            is_member = True if current_user in members else None
            members = members if len(members) > 0 else None
            return render_template(
                "event.html",
                event=event,
                group=group,
                members=members,
                is_member=is_member,
                is_event_admin=event.creator_id == current_user.id or group is not None and group.admin_id == current_user.id
            )

        elif action == 'join':
            if event.closed:
                Invitation.add(InvitationType.TO_EVENT,
                               recipient_id=event.id,
                               referrer_id=current_user.id,
                               expiration_time=event.time)
                flash(gettext("Invitation sent!"), "success")
            else:
                event.add_member(current_user)
            return redirect(url_for('event_route', action='show', id=event_id))

        elif action == 'leave':
            event.remove_member(current_user)
            return redirect(url_for('event_route', action='show', id=event_id))

        elif action == 'find_people':
            # FIXME сделать нормальный фильтр
            event_users = set(event.get_members())
            all_users = set(User.query.order_by(User.register_time).all())
            users: list = list(filter(lambda user_tmp: event.sport in user_tmp.sport, list(all_users - event_users)))
            return render_template("find_people.html", event_id=event.id, people=users if len(users) > 0 else None)

        else:
            abort(400)
# ------------------------------------------------------------------------------------------
# ------------------------------------- POST -----------------------------------------------
    elif request.method == 'POST':
        type = get_arg_or_400('type')

        if type == 'edit':
            event_id = get_arg_or_400('id', to_int=True)
            event = Event.get_or_404(event_id)
            edit_event_form = EditEventForm(current_event=event)
            if edit_event_form.validate_on_submit():
                event.closed = edit_event_form.closed.data
                event.name = edit_event_form.name.data
                event.description = edit_event_form.description.data
                event.sport = edit_event_form.sport.data
                event.time = edit_event_form.time.data
                db.session.add(event)
                db.session.commit()
                return redirect(url_for('event_route', action='show', id=event.id))
            else:
                return render_template("edit_event.html", form=edit_event_form, event=event)

        elif type == 'new':
            new_event_form = NewEventForm(groups=current_user.get_groups())
            if new_event_form.validate_on_submit():
                closed = new_event_form.closed.data
                name = new_event_form.name.data
                description = new_event_form.description.data
                sport = new_event_form.sport.data
                group_id = new_event_form.assigned_group.data
                group_id = None if group_id == "None" or group_id is None else int(group_id)
                time = new_event_form.time.data
                new_event = Event(
                    name=name,
                    description=description,
                    sport=sport,
                    group_id=group_id,
                    creation_time=timestamp(),
                    creator_id=current_user.id,
                    time=time,
                    closed=closed
                )
                db.session.add(new_event)
                db.session.commit()
                new_event_member = EventMember(event_id=new_event.id, user_id=current_user.id, time=timestamp())
                db.session.add(new_event_member)
                db.session.commit()
                return redirect(url_for('event_route', action='show', id=new_event.id))
            else:
                return render_template("new_event.html", form=new_event_form)
        else:
            abort(400)
    else:
        abort(403)
