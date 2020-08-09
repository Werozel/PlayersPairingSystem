from globals import app, get_arg_or_400
from flask_login import login_required
from flask import render_template, request, abort
from forms import SearchGroupForm
from libs.Group import Group


@app.route("/search_group", methods=['GET', 'POST'])
@login_required
def search_group_route():
    if request.method == 'GET':
        search_group_form = SearchGroupForm()
        sport = get_arg_or_400('sport')
        if sport is None:
            groups = Group.query.limit(30).all()
        else:
            groups = Group.get_by_sport(sport)
        return render_template("search_group.html", query=groups, form=search_group_form)
    elif request.method == 'POST':
        search_group_form = SearchGroupForm()
        name = search_group_form.name.data
        sport = search_group_form.sport.data
        groups = Group.query.filter(Group.name.ilike(f"%{name}%")).\
            filter(Group.sport == sport if sport != "None" else Group.sport == Group.sport).all()
        return render_template("search_group.html", query=groups, form=search_group_form)
    else:
        abort(403)