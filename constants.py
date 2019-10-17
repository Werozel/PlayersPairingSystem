
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

    selection = "Select sport:" + "\n"\
                "1 - " + tennis + "\n"\
                "2 - " + football + "\n"\
                "3 - " + basketball + "\n"\
                "4 - " + volleyball + "\n"\
                "5 - " + hockey + ": \n"


class Commands:
    help = ["help", "h"]
    register = ["reg", "register", "r"]
    create_group = ["create", "c", "create_group"]
    login = ["login", "l"]
    info = ["info", "i"]
    join = ["join", "join_group", "j"]
    exit = ["exit", "quit", "e", "q"]


class Responses:
    help = "register, reg, r - Creates a new user\n" \
           "login, l - Allows user to log in\n" \
           "info, i - Shows info about current user\n" \
           "create_group, create, c - Creates new group\n" \
           "join, j - Allows user to join an existing group\n" \
           "exit, quit, e, q - Exits program\n"

    exiting = "Exiting..."
    unknown_cmd = "Unknown command, try 'help'"
