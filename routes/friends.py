from globals import app
from src.misc import get_arg_or_400
from flask_login import login_required, current_user
from flask import render_template, abort
from libs.models.User import User
from libs.Vector import UserVector
from libs.models.PlayTime import PlayTime


@app.route("/friends", methods=['GET'])
@login_required
def friends_route():
    action = get_arg_or_400('action')
    if action == 'search':
        user_vector = UserVector(
            age=current_user.age,
            gender=current_user.gender,
            sport=current_user.sport,
            city=current_user.city,
            last_login=current_user.last_login,
            include_play_times=True,
            play_times=PlayTime.get_all_for_user_id(current_user.id),
            user=current_user
        )
        users = User.query.order_by(User.register_time).all()
        sorted_users = list(
            map(
                lambda x:  x[0].user,
                sorted(
                    map(
                        lambda x: (
                            x,
                            user_vector.calculate_diff_with_user(x)
                        ),
                        map(
                            lambda x: UserVector(
                                age=x.age,
                                gender=x.gender,
                                sport=x.sport,
                                city=x.city,
                                last_login=x.last_login,
                                include_play_times=True,
                                play_times=PlayTime.get_all_for_user_id(x.id),
                                user=x
                            ),
                            filter(
                                lambda x: x.id != current_user.id,
                                users
                            )
                        )
                    ),
                    key=lambda x: x[1],
                    reverse=True
                )
            )
        )
        return render_template("show_users.html", current_user=current_user, users=sorted_users)
    else:
        abort(400)
