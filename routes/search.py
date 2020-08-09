from globals import app
from flask_login import login_required
from flask import render_template, request
from forms import SearchGroupForm
from libs.Group import Group


@app.route("/search_group", methods=['GET', 'POST'])
@login_required
def search_group_route():
    search_group_form = SearchGroupForm()
    if request.method == 'GET':
        sport = request.args.get('sport')
        if sport is None:
            groups = Group.query.limit(30).all()
        else:
            groups = Group.get_by_sport(sport)
        return render_template("search_group.html", query=groups, form=search_group_form)
    elif request.method == 'POST':
        name = search_group_form.name.data
        sport = search_group_form.sport.data
        groups = Group.query.filter(Group.name.ilike(f"%{name}%")).\
            filter(Group.sport == sport if sport != "None" else Group.sport == Group.sport).all()
        return render_template("search_group.html", query=groups, form=search_group_form)
    else:
        groups = Group.query.limit(50).all()
        return render_template("search_group.html", query=groups, form=search_group_form)