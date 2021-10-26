import sys, logging
# Logging as output logging messages.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# all our PERSONAL variables are stored in here
import variables

try:
    from humidity import temp
    list_temp = temp()
except ImportError:
    list_temp = False
    logging.exception("Import Adafruit_DHT has failed!")

import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop

"""
"""


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/temp':
        if list_temp:
            bot.sendMessage(chat_id, "Here you have your temps and humidity values!")
            temp_1="Sensor 1: {0:0.1f}*C%".format(list_temp[0][0])
            temp_2="Sensor 2: {0:0.1f}*C%".format(list_temp[1][0])
            bot.sendMessage(chat_id, temp_1)
            bot.sendMessage(chat_id, temp_2)
        else:
            bot.sendMessage(chat_id, "RPI's sensors are not responding!")
            logging.error("RPI's sensors are not responding.")
    else:
        bot.sendMessage(chat_id, "Sorry, I did not quite understand...")

bot = telepot.Bot(variables.token_bot_api)


bot.sendMessage("Hi there! Im all awake!")
MessageLoop(bot, handle).run_as_thread()
logging.debug('I am listening ...')

while 1:
    time.sleep(10)
