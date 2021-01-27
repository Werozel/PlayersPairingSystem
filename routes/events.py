from typing import Optional, List

from globals import app, db, nominatim
from constants.constants import Sports
from src.misc import timestamp, get_arg_or_400, filter_not_none, get_arg_or_none, get_current_time, get_current_day_of_week, time_to_seconds
from flask_login import login_required, current_user
from flask_babel import gettext
from flask import render_template, request, redirect, url_for, flash, abort
from forms import EditEventForm, SearchEventForm, AddEventPlayTimeForm
from libs.models.Event import Event
from libs.models.EventMember import EventMember
from libs.models.Group import Group
from libs.models.User import User
from libs.models.Invitation import Invitation, InvitationType
from flask_googlemaps import Map
from libs.models.EventPlayTimes import EventPlayTimes
from libs.models.AddressCaches import Location, Address, LocationToAddress


@app.route("/event", methods=['GET', 'POST'])
@login_required
def event_route():
    if request.method == 'GET':

        action = get_arg_or_400('action')
        if action == 'my':
            events = filter_not_none(current_user.get_events())
            return render_template(
                "my_events.html",
                events=events if len(events) > 0 else None
            )

        elif action == 'new':
            new_event_form = EditEventForm(groups=filter_not_none(current_user.get_groups()))
            return render_template("new_event.html", form=new_event_form, map=get_loc_map())
        elif action == 'search':
            events = Event.query.all()
            form = SearchEventForm()
            return render_template(
                "search_event.html",
                events=events,
                form=form
            )

        event_id = get_arg_or_400('event_id', to_int=True)
        event: Event = Event.get_or_404(event_id)
        group = event.group
        group: Group = group if group else None
        is_event_admin = event.creator_id == current_user.id or group is not None and group.admin_id == current_user.id
        all_play_times = EventPlayTimes.get_all_for_event(event_id)

        if action == 'delete':
            event.delete()
            return redirect(url_for("event_route", action='my'))

        elif action == 'accept_invitation' or action == 'reject_invitation':
            if current_user.id != event.creator_id:
                abort(403)
            invitation = Invitation.get_or_404(get_arg_or_400('id'))
            if action == 'accept_invitation':
                invitation.accept()
            else:
                invitation.reject()
            return redirect(url_for("event_route", action='invitations', event_id=event_id))

        elif action == 'show_play_times':
            return render_template(
                "show_event_play_times.html",
                map=get_loc_map(event, EventPlayTimes.get_or_none(get_arg_or_none("play_time_id"))),
                all_play_times=all_play_times,
                is_event_admin=is_event_admin,
                event_id=event_id
            )

        elif action == 'add_play_time':
            add_event_play_time_form = AddEventPlayTimeForm()
            current_play_time: EventPlayTimes = EventPlayTimes.get_or_none(get_arg_or_none("play_time_id"))
            if current_play_time:
                add_event_play_time_form.day_of_week.data = current_play_time.day_of_week
                add_event_play_time_form.start_time.data = current_play_time.start_time
                add_event_play_time_form.end_time.data = current_play_time.end_time
                add_event_play_time_form.address.data = Address.get(current_play_time.address_id).get_short_address()
            template = render_template(
                "add_event_play_time.html",
                map=get_loc_map(event, current_play_time, "height:600px;width:650px;margin:8;"),
                form=add_event_play_time_form,
                all_play_times=all_play_times,
                event_id=event_id
            )
            return template

        elif action == 'edit':
            if not is_event_admin:
                abort(403)
            play_time: Optional[EventPlayTimes] = pt if (pt := all_play_times[0] if all_play_times else None) else None
            edit_event_form = EditEventForm(
                groups=filter_not_none(current_user.get_groups()),
                closed=event.closed,
                name=event.name,
                description=event.description,
                sport=event.sport,
                recurring=event.recurring,
                day_of_week=play_time.day_of_week if play_time else None,
                start_time=play_time.start_time if play_time else None,
                end_time=play_time.end_time if play_time else None,
                address=play_time.address.short_address if play_time and play_time.address else None
            )
            initial_location = Location.get(play_time.location_id) if play_time else None
            loc_map = Map(
                zoom=14.5 if initial_location else 2,
                identifier="loc_map",
                lat=initial_location.latitude if initial_location else 0,
                lng=initial_location.longitude if initial_location else 0,
                style="height:600px;width:600px;margin:8;",
                language=current_user.language,
                markers=[(initial_location.latitude, initial_location.longitude)] if initial_location else []
            )
            return render_template("edit_event.html", form=edit_event_form, event=event, map=loc_map)

        elif action == 'invitations':
            if not is_event_admin:
                abort(403)
            event_invitations: List[Invitation] = Invitation.get_all_for_event(event_id)
            return render_template("event_invitations.html", invitations=event_invitations, event_id=event_id)

        elif action == 'show':
            members = event.get_members()
            is_member = True if current_user in members else None
            members = members if len(members) > 0 else None
            play_time_id = get_arg_or_none('play_time_id')
            selected_play_time = None
            if play_time_id is not None:
                selected_play_time = EventPlayTimes.query.filter_by(event_id=event_id, id=play_time_id).first()
            if selected_play_time is None:
                play_times = EventPlayTimes.get_all_for_event(event_id)
                # closest_play_time: EventPlayTimes = play_times[0] if play_times and len(play_times) else None # TODO
                current_day_of_week = get_current_day_of_week()
                current_time = get_current_time()
                valid_play_times = list(
                    filter(
                        lambda x:
                        x.day_of_week is not None and
                        x.start_time is not None and
                        (
                            (x.day_of_week == current_day_of_week and time_to_seconds(x.start_time) >= current_time) or
                            x.day_of_week != current_day_of_week
                        ),
                        play_times
                    )
                )
                sorted_play_times = list(
                    sorted(
                        valid_play_times,
                        key=lambda x: -10 * abs(current_day_of_week - x.day_of_week) - abs(current_time - time_to_seconds(x.start_time)),
                    )
                ) \
                    if valid_play_times \
                    else None
                closest_play_time = sorted_play_times[0] if sorted_play_times else None
                initial_location = LocationToAddress.get_location_for_address_id(closest_play_time.address_id) \
                    if closest_play_time \
                    else None
                loc_map = Map(
                    zoom=14.5 if initial_location else 2,
                    identifier="loc_map",
                    lat=initial_location.latitude if initial_location else 0,
                    lng=initial_location.longitude if initial_location else 0,
                    style="height:600px;width:600px;margin:8;",
                    language=current_user.language,
                    markers=[(initial_location.latitude, initial_location.longitude)] if initial_location else []
                ) if initial_location else None
                return render_template(
                    "event.html",
                    event=event,
                    group=group,
                    members=members,
                    is_member=is_member,
                    event_id=event_id,
                    is_event_admin=is_event_admin,
                    play_times=all_play_times,
                    closest_play_time=closest_play_time,
                    map=loc_map
                )
            else:
                initial_address: Address = Address.get(selected_play_time.address_id) if selected_play_time else None
                initial_location = LocationToAddress.get_location_for_address_id(
                    selected_play_time.address_id) if selected_play_time else None
                loc_map = Map(
                    zoom=14.5 if initial_location else 2,
                    identifier="loc_map",
                    lat=initial_location.latitude if initial_location else 0,
                    lng=initial_location.longitude if initial_location else 0,
                    style="height:600px;width:600px;margin:8;",
                    language=current_user.language,
                    markers=[(initial_location.latitude, initial_location.longitude)] if initial_location else []
                )
                return render_template(
                    "event.html",
                    event=event,
                    group=group,
                    members=members,
                    is_member=is_member,
                    event_id=event_id,
                    is_event_admin=is_event_admin,
                    play_times=all_play_times,
                    map_address=initial_address.get_short_address() if initial_address else None,
                    map=loc_map
                )

        elif action == 'join':
            if event.closed:
                Invitation.add(
                    InvitationType.TO_EVENT,
                    recipient_id=event.id,
                    referrer_id=current_user.id,
                    expiration_time=event.time
                )
                flash(gettext("Invitation sent!"), "success")
            else:
                event.add_member(current_user)
            return redirect(url_for('event_route', action='show', event_id=event_id))

        elif action == 'leave':
            event.remove_member(current_user)
            return redirect(url_for('event_route', action='show', event_id=event_id))

        elif action == 'find_people':
            # FIXME сделать нормальный фильтр
            event_users = set(event.get_members())
            invited = list(
                filter(
                    lambda x: x,
                    map(
                        lambda x: User.get_or_none(x.recipient_id),
                        Invitation.get_all_from_event(event_id)
                    )
                )
            )
            all_users = set(User.query.order_by(User.register_time).all())
            users: list = list(
                filter(
                    lambda user_tmp: event.sport in (user_tmp.sport if user_tmp.sport else []),
                    list(all_users - event_users - set(invited))
                )
            )
            return render_template(
                "find_people.html",
                event_id=event.id,
                invited_people=invited,
                people=users if len(users) > 0 else None
            )
        elif action == 'send_invite':
            Invitation.add(
                type=InvitationType.FROM_EVENT,
                recipient_id=get_arg_or_400('user_id'),
                referrer_id=event_id
            )
            return redirect(url_for('event_route', action='find_people', event_id=event_id))
        elif action == 'revoke_invite':
            invitation = Invitation.query.filter(
                (Invitation.type==InvitationType.FROM_EVENT) &
                (Invitation.recipient_id==get_arg_or_400('user_id')) &
                (Invitation.referrer_id==event_id)
            ).first()
            if invitation:
                db.session.delete(invitation)
                db.session.commit()
            return redirect(url_for('event_route', action='find_people', event_id=event_id))
        else:
            abort(400)
# ------------------------------------------------------------------------------------------
# ------------------------------------- POST -----------------------------------------------
    elif request.method == 'POST':
        action = get_arg_or_400('action')

        if action == 'edit':
            event_id = get_arg_or_400('id', to_int=True)
            event = Event.get_or_404(event_id)
            edit_event_form = EditEventForm(current_event=event, groups=filter_not_none(current_user.get_groups()))
            if edit_event_form.validate_on_submit():
                event.closed = edit_event_form.closed.data
                event.name = edit_event_form.name.data
                event.description = edit_event_form.description.data
                event.sport = edit_event_form.sport.data
                event.recurring = edit_event_form.recurring.data
                db.session.add(event)
                db.session.commit()
                all_play_times = EventPlayTimes.get_all_for_event(event.id)
                last_play_time = all_play_times[0] if all_play_times else None
                if last_play_time:
                    db.session.delete(last_play_time)
                    db.session.commit()
                day_of_week = edit_event_form.day_of_week.data
                start_time = edit_event_form.start_time.data
                end_time = edit_event_form.end_time.data
                query = edit_event_form.address.data
                address = Address.get_by_query(query)[0] if query else None
                play_time = EventPlayTimes(
                    event_id=event.id,
                    day_of_week=day_of_week if day_of_week != "None" else None,
                    start_time=start_time,
                    end_time=end_time,
                    address_id=address.id if address else None,
                    location_id=LocationToAddress.get_location_for_address_id(address.id).id if address else None
                )
                db.session.add(play_time)
                db.session.commit()
                return redirect(url_for('event_route', action='show', event_id=event.id))
            else:
                return render_template("edit_event.html", form=edit_event_form, event=event, map=get_loc_map())

        elif action == 'new':
            new_event_form = EditEventForm(groups=filter_not_none(current_user.get_groups()))
            if new_event_form.validate_on_submit():
                closed = new_event_form.closed.data
                name = new_event_form.name.data
                description = new_event_form.description.data
                sport = new_event_form.sport.data
                group_id = new_event_form.assigned_group.data
                group_id = None if group_id == "None" or group_id is None else int(group_id)
                recurring = new_event_form.recurring.data
                new_event = Event(
                    name=name,
                    description=description,
                    sport=sport,
                    group_id=group_id,
                    creation_time=timestamp(),
                    creator_id=current_user.id,
                    closed=closed,
                    recurring=recurring
                )
                db.session.add(new_event)
                db.session.commit()
                day_of_week = new_event_form.day_of_week.data
                start_time = new_event_form.start_time.data
                end_time = new_event_form.end_time.data
                query = new_event_form.address.data
                address = Address.get_by_query(query)[0] if query else None
                play_time = EventPlayTimes(
                    event_id=new_event.id,
                    day_of_week=day_of_week if day_of_week != "None" else None,
                    start_time=start_time,
                    end_time=end_time,
                    address_id=address.id if address else None,
                    location_id=LocationToAddress.get_location_for_address_id(address.id).id if address else None
                )
                db.session.add(play_time)
                db.session.commit()
                new_event_member = EventMember(event_id=new_event.id, user_id=current_user.id, time=timestamp())
                db.session.add(new_event_member)
                db.session.commit()
                return redirect(url_for('event_route', action='show', event_id=new_event.id))
            else:
                return render_template("new_event.html", form=new_event_form, map=get_loc_map())
        elif action == 'search':
            search_event_form = SearchEventForm()
            name = search_event_form.name.data
            sport = search_event_form.sport.data
            events = Event.query.filter(Event.name.ilike(f"%{name}%")). \
                filter(Event.sport == sport if sport != "None" else Event.sport == Event.sport).all()
            return render_template(
                "search_event.html",
                events=events,
                form=search_event_form
            )
        elif action == "add_play_time":
            form = AddEventPlayTimeForm()
            event = Event.get_or_404(get_arg_or_400("event_id"))
            if form.validate_on_submit():
                city = event.creator.city
                address = form.address.data
                addresses: List[Address] = Address.get_by_query(address)
                if len(addresses) == 0:
                    query = f"{address}, {city}" if city is not None and city.lower() not in address.lower() else address
                    # TODO call google api
                    pass
                address_db_obj: Address = addresses[0]
                location_db_obj: Optional[Location] = LocationToAddress.get_location_for_address_id(address_db_obj.id)
                if location_db_obj is None:
                    # Такого быть не должно
                    # TODO call google api
                    pass

                event_play_time = EventPlayTimes(
                    day_of_week=form.day_of_week.data,
                    start_time=form.start_time.data,
                    end_time=form.end_time.data,
                    address_id=address_db_obj.id,
                    location_id=location_db_obj.id,
                    event_id=event.id
                )
                db.session.add(event_play_time)
                db.session.commit()
            return redirect(url_for('event_route', action='add_play_time', event_id=event.id))
        else:
            abort(400)
    else:
        abort(403)


def get_loc_map(event: Event, current_play_time: Optional[EventPlayTimes] = None, style: str = "height:600px;width:730px;margin:8;"):
    initial_zoom = 13
    initial_location = nominatim.geocode(event.creator.city)
    init_lat = initial_location.latitude if initial_location else None
    init_lng = initial_location.longitude if initial_location else None
    markers = []
    if current_play_time is not None:
        location = Location.get(current_play_time.location_id)
        if location is not None:
            markers.append((location.latitude, location.longitude))
            init_lat = location.latitude
            init_lng = location.longitude
            initial_zoom = 14.5
    return Map(
        zoom=initial_zoom,
        identifier="loc_map",
        lat=init_lat,
        lng=init_lng,
        style=style,
        language=current_user.language,
        markers=markers
    )
