import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import sys, logging

# Logging as output logging messages.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# all our PERSONAL variables are stored in here
import variables

# RPI temperatures functions
error_import = False
try:
    from humidity import return_ALL_DHT_temp_humid
except (ModuleNotFoundError, ImportError) as error:
    error_import = True
    logging.exception("Import Adafruit_DHT has failed! %s", error)

import temp_netatmo
import take_picture

"""
    TELEGRAM BoT (powered by Telebot)
"""

"""
    Definition of our MESSAGES
"""
command_not_found = ['This command does not exist!']
command_under_maintenance = ['This command is still under some developtment', 'Command not yet fully operational!']

"""
    Functions for our commands
"""
# /temp returns DHT and Netatmo temperature values.
def command_temp():
    output_message = "Here you have your temps and humidity values!\n"
    # RPis temps
    if error_import:
        #bot.sendMessage(chat_id, "RPI's sensors are not responding!")
        output_message += "RPI's sensors are not responding!\n"
        logging.info("RPI's sensors are not responding.")
    else:
        list_temp = return_ALL_DHT_temp_humid()
        temp_1="Sensor 1: {0:0.1f}_C and {0:0.1f}% humidity".format(list_temp[0][0],list_temp[0][1])
        temp_2="Sensor 2: {0:0.1f}_C and {0:0.1f}% humidity".format(list_temp[1][0],list_temp[1][1])
        output_message += temp_1 + "\n"
        output_message += temp_2 + "\n"
        #bot.sendMessage(chat_id, temp)
    # Netatmo temps!
    output_message += "NETATMO: " + str(temp_netatmo.netatmo_room_temp() + "_C")
    # send message outthere
    return output_message

# /whereis return GPS location of a person. person ID is hard coded
def command_whereis():
    output_message = "Here are they:\n"
    return random.choice(command_under_maintenance)

# /takepic sends a pic taken from our webcamera
def command_takepic(chat_id):
    message = "Here you have your image!"
    bot.sendMessage(chat_id, message)
    bot.sendPhoto(chat_id, photo=open(take_picture.path_to_pic(), 'rb'))


def command_torrent(args):
    return random.choice(command_under_maintenance)



"""
    Handle function!
"""
# handle. finds and execute a command msg from client.
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].split()[0]    # we split text and take first value
    args = msg['text'].split()[1:]      # list of arguments -first element

    logging.info('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/temp':    # /temp command
        bot.sendMessage(chat_id, command_temp())
    elif command == "/whereis":
        bot.sendMessage(chat_id, command_whereis())
    elif command == "/takepic":
        command_takepic(chat_id)
    elif command == "/torrent":
        bot.sendMessage(chat_id,  command_torrent(args))
    else:
        bot.sendMessage(chat_id, "Sorry, I did not quite understand...")

"""
    Connecting to BoT!
"""
bot = telepot.Bot(variables.token_bot_api)

"""
    Bot is booted and welcome message!
"""
# Welcome message! we just started up!
bot.sendMessage(variables.bot_chat_id, "Hi there! Im all awake!")

MessageLoop(bot, handle).run_as_thread()
logging.info('I am listening ...')

while 1:
    time.sleep(10)
