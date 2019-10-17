
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
    register = ["reg", "register"]
    create_group = ["create", "c", "create_group", "new_group"]
    login = ["login", "l"]
    info = ["info", "i"]
    exit = ["exit", "quit", "e", "q"]


class Responses:
    help = "According to all known laws of aviation, there is no way a bee should be able to fly."

    exiting = "Exiting..."
    unknown_cmd = "Unknown command, try 'help'"
