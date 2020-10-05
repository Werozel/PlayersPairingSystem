from typing import Optional, List
from geopy import Location
from globals import app, db, google_api
from flask_login import current_user
from libs.models.PlayTime import PlayTime
from flask_babel import gettext as _
from flask import request, abort
from libs.models.AddressCaches import Address, Location as LocationDB, LocationToAddress
from langdetect import detect


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


def find(pred, coll):
    for x in coll:
        if pred(x):
            return x


@app.route("/api/map", methods=["POST"])
def get_location_by_address_route():
    if not current_user.is_authenticated:
        return {'success': False, 'msg': _("User not authenticated")}
    address = request.json.get("address")
    if address is None:
        abort(400)
    city: str = current_user.city
    query: str = f"{address}, {city}" if city is not None and city.lower() not in address.lower() else address
    res_from_cache: Optional[LocationDB] = LocationToAddress.get_location_for_address(address)
    if res_from_cache is not None:
        addresses_db_obj: List[Address] = LocationToAddress.get_address_for_location(
            res_from_cache.latitude,
            res_from_cache.longitude
        )
        return {
            'success': True,
            'address': address if len(addresses_db_obj) == 0 else addresses_db_obj[0].get_short_address(),
            'latitude': res_from_cache.latitude,
            'longitude': res_from_cache.longitude
        }
    try:
        result: Optional[Location] = google_api.geocode(
            query,
            language=detect(query)
        )
        if result is None:
            return {'success': False, 'msg': _("Nothing found!")}
        else:
            address_components: List[dict] = result.raw.get('address_components')
            country_component: dict = find(lambda x: 'country' in x.get('types'), address_components)
            city_component: dict = find(lambda x: 'locality' in x.get('types'), address_components)
            street_component: dict = find(lambda x: 'route' in x.get('types'), address_components)
            building_number_component: dict = find(lambda x: 'street_number' in x.get('types'), address_components)
            address_db_obj = Address(
                full_address=result.address,
                custom_address=address,
                country=country_component.get('long_name') if country_component is not None else None,
                city=city_component.get('long_name') if city_component is not None else None,
                street=street_component.get('long_name') if street_component is not None else None,
                building_number=building_number_component.get('long_name')
                if building_number_component is not None
                else None
            )
            address_db_obj.short_address = address_db_obj.get_short_address()
            location_db_obj = LocationDB(
                latitude=result.latitude,
                longitude=result.longitude
            )
            db.session.add(address_db_obj)
            db.session.add(location_db_obj)
            db.session.commit()
            location_to_address_db_obj = LocationToAddress(address_id=address_db_obj.id, location_id=location_db_obj.id)
            db.session.add(location_to_address_db_obj)
            db.session.commit()
            return {
                'success': True,
                'latitude': result.latitude,
                'longitude': result.longitude,
                'address': address_db_obj.short_address
            }
    except Exception:
        return {'success': False, 'msg': _("Couldn't perform geocoding")}
