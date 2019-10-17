import globals
import logging, traceback
import requests
from constants import Sports, Commands, Responses
from Users import User
from Groups import Group


try:
    current_user = None
    while not globals.exiting:
        cmd = input("Enter a command: ").split(' ')
        if cmd[0] in Commands.help:
            print(Responses.help)
        elif cmd[0] in Commands.register:
            name = input("Name - ")
            last_name = input("Last name - ")
            age = int(input("Age - "))
            gender = input("Gender - ")
            sport = [Sports.get(int(i)) for i in input(Sports.selection).split(' ')]
            login = input("Login - ")
            psw = input("Password - ")
            current_user = User(name=name, last_name=last_name, age=age, gender=gender,
                     sport=sport, login=login, psw=psw)
            current_user.upload()
        elif cmd[0] in Commands.login:
            login = input("Login - ")
            psw = input("Password - ")
            cursor = globals.connection.cursor()
            cursor.execute(requests.login_req, [login, psw])
            data = cursor.fetchone()
            if data:
                current_user = User.get(data[0])
            else:
                print("Invalid login!")
            cursor.close()
        elif cmd[0] in Commands.info:
            if current_user:
                current_user.print()
            else:
                print("You need to log in first!")
        elif cmd[0] in Commands.create_group:
            if current_user:
                sport = Sports.get(int(input(Sports.selection)))
                admin = current_user.id
                g = Group(admin=User.get(admin), members=[User.get(admin)], sport=sport)
                current_user.admined_groups.append(g.id)
                current_user.upload()
                g.upload()
            else:
                logging.error("You need to log in first")
        elif cmd[0] in Commands.exit:
            print(Responses.exiting)
            globals.exiting = 1
        else:
            print(Responses.unknown_cmd)
except Exception as e:
    print(traceback.format_exc())
    logging.warning("Exiting...")


globals.finish()
