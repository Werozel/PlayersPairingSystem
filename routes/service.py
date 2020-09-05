from globals import app, db
from flask_login import current_user, AnonymousUserMixin
from flask import request, redirect, make_response
from src.misc import get_arg_or_none
from constants.constants import LANGUAGES


@app.route("/change_language")
def change_language_route():
    new_language = get_arg_or_none('language')
    if new_language not in LANGUAGES:
        curr_language = request.cookies.get('language')
        if curr_language == 'en':
            new_language = 'ru'
        else:
            new_language = 'en'
    resp = make_response(redirect(request.referrer))
    resp.set_cookie('language', new_language)
    if current_user.is_authenticated:
        current_user.language = new_language
        db.session.add(current_user)
        db.session.commit()
    return resp
