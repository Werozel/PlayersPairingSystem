from globals import app, db
from flask_login import current_user
from libs.models.PlayTime import PlayTime


@app.route("/api/play_time_del/<int:id>", methods=["DELETE"])
def play_time_route(id: int):
    play_time = PlayTime.get(id)
    if play_time is None:
        return {'success': False, 'msg': "No such play time"}
    if not current_user.is_authenticated or play_time.user_id != current_user.id:
        return {'success': False, 'msg': "Not allowed"}
    db.session.delete(play_time)
    db.session.commit()
    return {'success': True}
