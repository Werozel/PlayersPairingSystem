from globals import app, db, sessions
from src.misc import get_arg_or_400
from src.youtube_links import make_link, parse_id
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, abort
from flask_babel import gettext
from forms import EditProfileForm, EditVideosForm
from libs.models.User import User
from libs.models.ChatMember import ChatMember
from libs.models.Invitation import Invitation, InvitationType
from libs.models.PlayTimes import PlayTimes
from libs.models.User import set_user_picture
from libs.models.UserToSportToVideo import UserToSportToVideo
from flask_socketio import emit
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
            videos: dict = UserToSportToVideo.get_all_for_user_id(current_user.id)
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
            videos: dict = UserToSportToVideo.get_all_for_user_id(user.id)
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
                times_values=PlayTimes.get_all_for_user_id(current_user.id)
            )
            return render_template("edit_profile.html", title="Edit profile", form=form, current_user=current_user)
        elif action == 'edit_videos':
            group = namedtuple('Group', ['sport', 'video'])
            videos = UserToSportToVideo.get_all_for_user_id(current_user.id)
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
                emit('invitation', json.dumps({'invitation_id': invitation_id}), room=sessions.get(new_friend_id))
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
                if len(form.sport.data):
                    current_user.sport = form.sport.data
                db.session.add(current_user)
                # for data in form.times.data:
                #     id = data.get('play_time_id')
                #     play_time = None
                #     if id:
                #         play_time = PlayTimes.get(id)
                #     if play_time:
                #         play_time.day_of_week = data.get('day_of_week')
                #         play_time.start_time = data.get('start_time')
                #         play_time.end_time = data.get('end_time')
                #     else:
                #         play_time = PlayTimes(
                #             day_of_week=data.get('day_of_week'),
                #             start_time=data.get('start_time'),
                #             end_time=data.get('end_time'),
                #             user_id=current_user.id
                #         )
                #     db.session.add(play_time)
                db.session.commit()
                flash(gettext("Profile updated!"), 'success')
                return redirect(url_for('profile_route', action='my'))
            else:
                return render_template("edit_profile.html", form=form, current_user=current_user)
        elif action == 'edit_videos':
            form = EditVideosForm()
            if form.validate_on_submit():
                for video_entry in form.videos.entries:
                    user_to_sport_to_video = UserToSportToVideo.get_video(current_user.id, video_entry.sport.data)
                    if user_to_sport_to_video is None:
                        if video_entry.video.data is None or len(video_entry.video.data) == 0:
                            continue
                        user_to_sport_to_video = UserToSportToVideo(
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
        else:
            form = EditProfileForm()
            return render_template("edit_profile.html", form=form, current_user=current_user)

    else:
        abort(403)
