from typing import Optional
from geopy import Location
from src.misc import get_cookie
from globals import app, db, google_api
from flask_login import current_user
from libs.models.PlayTime import PlayTime
from flask_babel import gettext as _
from src.address_cache import address_cache


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


@app.route("/api/map/<string:address>", methods=["GET"])
def get_location_by_address_route(address: str):
    if not current_user.is_authenticated:
        return {'success': False, 'msg': "User not authenticated"}
    city: str = current_user.city
    query: str = f"{city} {address}" if city is not None and city.lower() not in address.lower() else address
    res_from_cache = address_cache.get(query)
    if res_from_cache is not None:
        return {'success': True, **res_from_cache}
    try:
        result: Optional[Location] = google_api.geocode(
            query,
            language=current_user.language
            if current_user.language and len(current_user.language) != 0
            else get_cookie('language', 'ru')
        )
        if result is None:
            return {'success': False, 'msg': _("Nothing found!")}
        else:
            location_obj = {
                'latitude': result.latitude,
                'longitude': result.longitude,
                'address': result.address
            }
            address_cache.update({query: location_obj, result.address: location_obj})
            return {
                'success': True,
                **location_obj
            }
    except Exception:
        return {'success': False, 'msg': _("Couldn't perform geocoding")}
