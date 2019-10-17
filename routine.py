import globals
import logging
import constants
from constants import Sports, Commands, Responses
from Users import User
from Groups import Group

try:
    while not globals.exiting:
        cmd = input("Enter a command: ").partition(' ')
        if cmd[0] == Commands.help:
            print(Responses.help)
        elif cmd[0] == Commands.exit:
            print(Responses.exiting)
            globals.exiting = 1
        else:
            print(Responses.unknown_cmd)
except:
    logging.warning("Exiting...")

globals.finish()
