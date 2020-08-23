import calendar
from typing import Optional


class Sports:
    tennis = "Tennis"
    football = "Football"
    basketball = "Basketball"
    volleyball = "Volleyball"
    hockey = "Hockey"

    @staticmethod
    def get(n):
        return {
            1: Sports.tennis,
            2: Sports.football,
            3: Sports.basketball,
            4: Sports.volleyball,
            5: Sports.hockey
        }.get(n, None)

    @staticmethod
    def get_list():
        return [Sports.tennis, Sports.football, Sports.basketball, 
                Sports.volleyball, Sports.hockey]

    @staticmethod
    def get_choices():
        return [(i, i) for i in Sports.get_list()]

    selection = "Select sport:" + "\n"\
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
