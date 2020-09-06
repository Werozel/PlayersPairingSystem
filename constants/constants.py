import calendar
from typing import Optional
from flask_babel import gettext as _


LANGUAGES = [
    'en',
    'ru'
]


DATETIME_FORMATS = {
    'en': ["EEEE, MMM dd, HH:mm", "EEEE, MMM dd YY, HH:mm"],
    'ru': ["EEEE, dd MMM, HH:mm", "EEEE, dd MMM YY, HH:mm"]
}


class Sports:
    tennis = _("Tennis")
    football = _("Football")
    basketball = _("Basketball")
    volleyball = _("Volleyball")
    hockey = _("Hockey")

    tennis_raw = "Tennis"
    football_raw = "Football"
    basketball_raw = "Basketball"
    volleyball_raw = "Volleyball"
    hockey_raw = "Hockey"

    @staticmethod
    def get(n):
        return {
            1: Sports.tennis_raw,
            2: Sports.football_raw,
            3: Sports.basketball_raw,
            4: Sports.volleyball_raw,
            5: Sports.hockey_raw
        }.get(n, None)

    @staticmethod
    def get_list():
        return [Sports.tennis_raw, Sports.football_raw, Sports.basketball_raw,
                Sports.volleyball_raw, Sports.hockey_raw]

    @staticmethod
    def get_choices():
        return [(i, _(i)) for i in Sports.get_list()]

    selection = _("Select sport") + ":" + "\n"\
                "1 - " + tennis + "\n"\
                "2 - " + football + "\n"\
                "3 - " + basketball + "\n"\
                "4 - " + volleyball + "\n"\
                "5 - " + hockey + "\n"


class Commands:
    help = ["help", "h"]
    register = ["reg", "register", "r"]
    create_group = ["create", "c", "create_group"]
    login = ["login", "l"]
    info = ["info", "i"]
    info_group = ["info_group", "ig"]
    join = ["join", "join_group", "j"]
    exit = ["exit", "quit", "e", "q"]


class Responses:
    help = "register, reg, r - Creates a new user\n" \
           "login, l - Allows user to log in\n" \
           "info, i - Shows info about current user\n" \
           "info_group, ig - Show info about group\n" \
           "create_group, create, c - Creates new group\n" \
           "join, j - Allows user to join an existing group\n" \
           "exit, quit, e, q - Exits program\n"

    exiting = "Exiting..."
    unknown_cmd = "Unknown command, try 'help'"


class DayOfWeek:
    days_of_week = [(i, calendar.day_name[i]) for i in range(0, 7)]

    @staticmethod
    def get_name(i: int) -> Optional[str]:
        if i < 0 or i >= 7:
            return None
        return DayOfWeek.days_of_week.__getitem__(i).second()
