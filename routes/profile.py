from typing import Optional, List

from globals import app, db, sessions, socketIO, nominatim
from flask_googlemaps import Map
from src.misc import get_arg_or_400, get_arg_or_none
from src.youtube_links import make_link, parse_id
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, abort
from flask_babel import gettext
from forms import EditProfileForm, EditVideosForm, AddPlayTimeForm
from libs.models.User import User
from libs.models.ChatMember import ChatMember
from libs.models.Invitation import Invitation, InvitationType
from libs.models.PlayTime import PlayTime
from libs.models.User import set_user_picture
from libs.models.UserVideos import UserVideos
from libs.models.AddressCaches import Address, Location, LocationToAddress
from collections import namedtuple
import json


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile_route():
    if request.method == 'GET':
        action = get_arg_or_400('action')
        if action == 'my':
            groups = current_user.get_groups()
            friends = current_user.friends_get()
            videos: dict = UserVideos.get_all_for_user_id(current_user.id)
            return render_template(
                "profile.html",
                current_user=current_user,
                user=current_user,
                groups=groups,
                friends=friends,
                my=True,
                videos=videos
            )
        elif action == 'show':
            id = get_arg_or_400('id', to_int=True)
            if current_user.id == id:
                return redirect(url_for('profile_route', action='my'))
            user = User.get_or_404(id)
            groups = user.get_groups()
            friends = user.friends_get()
            chat = ChatMember.get_private_chat(current_user.id, id)
            is_friend = True if current_user in friends else None
            videos: dict = UserVideos.get_all_for_user_id(user.id)
            return render_template(
                "profile.html",
                chat_id=chat.id if chat else None,
                current_user=current_user,
                groups=groups,
                friends=friends,
                is_friend=is_friend,
                user=user,
                videos=videos
            )
        elif action == 'edit':
            form = EditProfileForm(
                name=current_user.name,
                last_name=current_user.last_name,
                age=current_user.age,
                gender=current_user.gender,
                sport=current_user.sport,
                times_values=PlayTime.get_all_for_user_id(current_user.id)
            )
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
        elif action == 'add_play_time':
            add_play_time_form = AddPlayTimeForm()
            all_play_times = PlayTime.get_all_for_user_id(current_user.id)
            current_play_time: Optional[PlayTime] = PlayTime.get(get_arg_or_none("id"))
            initial_location = nominatim.geocode(current_user.city)
            init_lat = initial_location.latitude
            init_lng = initial_location.longitude
            markers = []
            initial_zoom = 13
            if current_play_time is not None:
                add_play_time_form.day_of_week.data = current_play_time.day_of_week
                add_play_time_form.start_time.data = current_play_time.start_time
                add_play_time_form.end_time.data = current_play_time.end_time
                add_play_time_form.address.data = current_play_time.address.short_address
                location = Location.get(current_play_time.location_id)
                if location is not None:
                    markers.append((location.latitude, location.longitude))
                    init_lat = location.latitude
                    init_lng = location.longitude
                    initial_zoom = 14.5
            loc_map = Map(
                zoom=initial_zoom,
                identifier="loc_map",
                lat=init_lat,
                lng=init_lng,
                style="height:600px;width:600px;margin:8;",
                language=current_user.language,
                markers=markers
            )
            return render_template(
                "add_play_time.html",
                all_play_times=all_play_times,
                form=add_play_time_form,
                map=loc_map
            )
        elif action == 'show_play_times':
            initial_zoom = 13
            initial_location = nominatim.geocode(current_user.city)
            init_lat = initial_location.latitude
            init_lng = initial_location.longitude
            markers = []
            current_play_time: Optional[PlayTime] = PlayTime.get(get_arg_or_none("id"))
            if current_play_time is not None:
                location = Location.get(current_play_time.location_id)
                if location is not None:
                    markers.append((location.latitude, location.longitude))
                    init_lat = location.latitude
                    init_lng = location.longitude
                    initial_zoom = 14.5
            loc_map = Map(
                zoom=initial_zoom,
                identifier="loc_map",
                lat=init_lat,
                lng=init_lng,
                style="height:600px;width:730px;margin:8;",
                language=current_user.language,
                markers=markers
            )
            user_id = get_arg_or_400('user_id', to_int=True)
            all_play_times = PlayTime.get_all_for_user_id(user_id)
            return render_template(
                "show_play_times.html",
                map=loc_map,
                all_play_times=all_play_times,
                user_id=user_id
            )
        elif action == 'edit_videos':
            group = namedtuple('Group', ['sport', 'video'])
            videos = UserVideos.get_all_for_user_id(current_user.id)
            arr = [group(sport, (make_link(vid) if (vid := videos.get(sport)) is not None else "")) for sport in current_user.sport]
            form = EditVideosForm(data={'videos': arr})
            return render_template("edit_videos.html", form=form, current_user=current_user)
        elif action == 'friend_add':
            new_friend_id = get_arg_or_400('id', to_int=True)
            invitation_id = Invitation.add(
                InvitationType.FRIEND,
                referrer_id=current_user.id,
                recipient_id=new_friend_id
            )
            if invitation_id != -1:
                room = sessions.get(new_friend_id)
                if room:
                    socketIO.emit('invitation', json.dumps({'invitation_id': invitation_id}), room=room)
                flash(gettext("Invitation sent!"), "success")
            else:
                flash(gettext("You already sent an invitation to this user!"), "info")
            return redirect(url_for("profile_route", action='show', id=new_friend_id))
        elif action == 'friend_remove':
            id = get_arg_or_400('id', to_int=True)
            current_user.friend_remove(id)
            flash(gettext("Friend removed!"), "success")
            return redirect(url_for("profile_route", action='show', id=id))
        else:
            abort(400)

    elif request.method == 'POST':
        action = get_arg_or_400('action')
        if action == 'edit_profile':
            form = EditProfileForm()
            if form.validate_on_submit():
                if form.picture.data:
                    set_user_picture(form.picture.data)
                current_user.name = form.name.data
                current_user.last_name = form.last_name.data
                current_user.age = form.age.data
                current_user.gender = form.gender.data
                current_user.city = form.city.data
                if len(form.sport.data):
                    current_user.sport = form.sport.data
                db.session.add(current_user)
                db.session.commit()
                flash(gettext("Profile updated!"), 'success')
                return redirect(url_for('profile_route', action='my'))
            else:
                return render_template("edit_profile.html", form=form, current_user=current_user)
        elif action == 'edit_videos':
            form = EditVideosForm()
            if form.validate_on_submit():
                for video_entry in form.videos.entries:
                    user_to_sport_to_video = UserVideos.get_video(current_user.id, video_entry.sport.data)
                    if user_to_sport_to_video is None:
                        if video_entry.video.data is None or len(video_entry.video.data) == 0:
                            continue
                        user_to_sport_to_video = UserVideos(
                            user_id=current_user.id,
                            sport=video_entry.sport.data,
                            video_id=parse_id(video_entry.video.data)
                        )
                    else:
                        if video_entry.video.data is None or len(video_entry.video.data) == 0:
                            db.session.delete(user_to_sport_to_video)
                            db.session.commit()
                            continue
                        if user_to_sport_to_video.video_id == video_entry.video.data:
                            continue
                        user_to_sport_to_video.video_id = parse_id(video_entry.video.data)
                    db.session.add(user_to_sport_to_video)
                    db.session.commit()
                return redirect(url_for('profile_route', action='my'))
            else:
                return render_template("edit_videos.html", form=form, current_user=current_user)
        elif action == 'add_play_time':
            form = AddPlayTimeForm()
            if form.validate_on_submit():
                city = current_user.city
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

                play_time = PlayTime(
                    day_of_week=form.day_of_week.data,
                    start_time=form.start_time.data,
                    end_time=form.end_time.data,
                    address_id=address_db_obj.id,
                    location_id=location_db_obj.id,
                    user_id=current_user.id
                )
                db.session.add(play_time)
                db.session.commit()
            return redirect(url_for('profile_route', action='add_play_time'))
        else:
            form = EditProfileForm()
            return render_template("edit_profile.html", form=form, current_user=current_user)

    else:
        abort(403)
