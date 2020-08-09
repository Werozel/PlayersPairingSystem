from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask import abort
from src.misc import is_admin


def get_admin(cur_app, cur_db) -> Admin:
    from libs.models.User import User
    from libs.models.Group import Group
    from libs.models.Event import Event
    res = Admin(cur_app, index_view=SecureAdminIndexView())
    res.add_view(SecureModelView(User, cur_db.session))
    res.add_view(SecureModelView(Group, cur_db.session))
    res.add_view(SecureModelView(Event, cur_db.session))
    return res


class SecureAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return is_admin()

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class SecureModelView(ModelView):

    def is_accessible(self):
        return is_admin()

    def inaccessible_callback(self, name, **kwargs):
        abort(404)
