import logging, traceback
from constants import requests
from libs import crypto
import globals
from constants.constants import Sports, Commands, Responses
from libs.Users import User, login
from libs.Groups import Group


try:
    current_user = None
    while not globals.exiting:
        cmd = input("> Enter a command: ").split(' ')
        if cmd[0] in Commands.help:
            print(Responses.help)
        elif cmd[0] in Commands.register:
            login = input("Login - ")
            cursor = globals.connection.cursor()
            cursor.execute(requests.check_user_login, [login])
            data = cursor.fetchone()
            cursor.close()
            if data:
                print("This login already taken!")
                continue
            psw = crypto.hash(input("Password - "))
            name = input("Name - ")
            last_name = input("Last name - ")
            age = int(input("Age - "))
            gender = input("Gender - ")
            sport = [Sports.get(int(i)) for i in input(Sports.selection).split(' ')]
            current_user = User(name=name, last_name=last_name, age=age, gender=gender,
                     sport=sport, login=login, psw=psw)
            current_user.upload()
        elif cmd[0] in Commands.login:
            username = input("Login - ")
            password = crypto.hash(input("Password - "))
            current_user = login(username, password)
            if current_user:
                current_user.update_time()
                print("Login successful!")
            else:
                print("Invalid login!")
        elif cmd[0] in Commands.info:
            if current_user:
                current_user.print()
            else:
                print("You need to log in first!")
        elif cmd[0] in Commands.info_group:
            if len(cmd) > 1 and cmd[1] == "-all":
                cursor = globals.connection.cursor()
                cursor.execute(requests.get_all_groups)
                data = cursor.fetchall()
                cursor.close()
                for i in data:
                    print(Group.get(int(i[0])).tuple())
            else:
                Group.get(int(input("Enter group id - "))).print()
        elif cmd[0] in Commands.join:
            if not current_user:
                print("You need to login first!")
                continue
            sport = Sports.get(int(input(Sports.selection)))
            cursor = globals.connection.cursor()
            cursor.execute(requests.show_groups, [sport])
            data = cursor.fetchall()
            cursor.close()
            s = "Select group id:\n"
            for i in data:
                s += str(Group.get(i[0]).tuple()) + "\n"
            print(s)
            id = int(input())
            g = Group.get(id)
            if g:
                g.add_users(current_user.id)
                g.upload()
                current_user.add_group(g.id)
                current_user.upload()
            else:
                print("No such group id")
        elif cmd[0] in Commands.create_group:
            if current_user:
                sport = Sports.get(int(input(Sports.selection)))
                name = input("Name - ")
                admin = current_user.id
                g = Group(admin=User.get(admin), members=[User.get(admin)], sport=sport, name=name)
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
