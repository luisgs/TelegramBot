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
    error_import = True
    from humidity import return_ALL_DHT_temp_humid
except (ModuleNotFoundError, ImportError) as error:
    logging.exception("Import Adafruit_DHT has failed! %s", error)

import temp_netatmo


"""
"""


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    logging.info('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/temp':
        output_message = "Here you have your temps and humidity values!\n"
        # RPis temps
        if not error_import:
            list_temp = return_ALL_DHT_temp_humid()
            temp_1="Sensor 1: {0:0.1f}*C%".format(list_temp[0][0])
            temp_2="Sensor 2: {0:0.1f}*C%".format(list_temp[1][0])
            output_message += temp_1 + "\n"
            output_message += temp_2 + "\n"
            #bot.sendMessage(chat_id, temp)
        else:
            #bot.sendMessage(chat_id, "RPI's sensors are not responding!")
            output_message += "RPI's sensors are not responding!\n"
            logging.info("RPI's sensors are not responding.")

        # Netatmo temps!
        output_message += "NETATMO: " + str(temp_netatmo.netatmo_room_temp())
        # send message outthere
        bot.sendMessage(chat_id, output_message)
    else:
        bot.sendMessage(chat_id, "Sorry, I did not quite understand...")

bot = telepot.Bot(variables.token_bot_api)


# Welcome message! we just started up!
bot.sendMessage(variables.bot_chat_id, "Hi there! Im all awake!")

MessageLoop(bot, handle).run_as_thread()
logging.info('I am listening ...')

while 1:
    time.sleep(10)
