import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import sys
import logging
import os
import requests
# import urllib2

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
import device_location_traccar

"""
    TELEGRAM BoT (powered by Telebot)
"""

"""
    Definition of our MESSAGES
"""
# BoT booted up!
welcome_messages = ['Hi, How can I help you!',
                    'Hi, Im all awake and ready for you!',
                    'I was taking a nap but now Im ready, tell me!?']
# Command not found
command_not_found = ['This command does not exist!',
                     'Sorry, this command is... different, try again!',
                     'No idea what command this one is... try again']
command_under_maintenance = ['This command is still under some developtment',
                             'Command not yet fully operational!',
                             'Im still working on this one... I need time!',
                             'try again in a couple of weeks... :)']


"""
    Functions for our commands
"""


# /temp returns DHT and Netatmo temperature values.
def command_temp():
    output_message = "Here you have your temps and humidity values!\n"
    # RPis temps
    if error_import:
        # bot.sendMessage(chat_id, "RPI's sensors are not responding!")
        output_message += "RPI's sensors are not responding!\n"
        logging.info("RPI's sensors are not responding.")
    else:
        list_temp = return_ALL_DHT_temp_humid()
        temp_1 = "Sensor INTERNO: {0:0.1f}°C and {1:0.1f}% humidity".format(list_temp[0][0],list_temp[0][1])
        temp_2 = "Sensor EXTERNO: {0:0.1f}°C and {1:0.1f}% humidity".format(list_temp[1][0],list_temp[1][1])
        output_message += temp_1 + "\n"
        output_message += temp_2 + "\n"
        # bot.sendMessage(chat_id, temp)
    # Netatmo temps!
    output_message += "NETATMO: "+str(temp_netatmo.netatmo_room_temp())+"°C\n"

    # Cities' temperatures:
    cities = ['Madrid', 'Prague']
    for city in cities:
        request = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + variables.openwaether_api)
        weather = request.json()
        # logging.info("Current Temp at " + city + "is: " + str(weather['main']['temp']-273) + " Celsius")
        output_message += "Temperature in "\
                          + city\
                          + ": "\
                          + str(round(weather['main']['temp'] - 273.15, 1))\
                          + "°C, real feel: "\
                          + str(round(weather['main']['feels_like'] - 273.15, 1))\
                          + "°C\n"
        logging.info("Temperature in "
                     + city
                     + " is "
                     + str(round(weather['main']['temp'] - 273.15, 1)))

    # send message outthere
    return output_message

# /whereis return GPS location of a person. person ID is hard coded
def command_whereis():
    output_message = "Here are your device:\n"
    latitude, longitude = device_location_traccar.device_lat_long(variables.traccar_mydevice)

    output_message += "Latitude: " + str(latitude) + "\n"
    output_message += "Longitude: " + str(longitude) + "\n"

    # Create location image:
    base_url = "https://www.mapquestapi.com/staticmap/v4/getplacemap?"
    key = "key=" + variables.osm_api
    location = "&location=" + str(latitude) + "," + str(longitude) + "&size=600,300&type=map&zoom=16&imagetype=jpeg&scalebar=true&scalebarPos=top&showicon=mcenter"

    output_message += "Here is a link: \n"
    output_message += base_url + key + location

    return output_message


# /takepic sends a pic taken from our webcamera
def command_takepic(chat_id):
    message = "Let me take a picture for you. It might take a bit..."
    bot.sendMessage(chat_id, message)
    bot.sendPhoto(chat_id, photo=open(take_picture.path_to_pic(), 'rb'))


# COMMAND: /torrent
# COMMENT: ACCEPT torrent file or torrent's URL and add it to Torrent Client.
def command_torrent(args):
    return random.choice(command_under_maintenance)


# COMMAND: /status
# COMMENT: RETURN status of a serie of services.
# RETURN: String with status of services
def command_status(args):
    list_services = ["telegram_bot", "prometheus", "transmission-daemon"]
    # flexget, noip2
    output_message = "Here are your services' satus:\n"
    # if status == 0 -> it is running
    # eoc. it is NOT running
    for service in list_services:
        status = os.system('systemctl is-active --quiet ' + service)
        if (status == 0):  # Service is running!
            output_message += service + " is running!\n"
            logging.info(service + "is running!")
        else:
            output_message += service + " is NOT running!\n"
            logging.info(service + "is NOT running!")

    # External IP Address!
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    output_message += 'My public IP address is: {}'.format(ip)

    return output_message


# List of developed commands.
# list_commands = [(command_ID, ["command_string", "definition_explantion"])]
list_commands = {"/roll": "Roll dice returns a random number between 1 and 6",
                 "/time": "Returns date and time.",
                 "/temp": "Returns temperature and humidity values from our DHT and Netatmo sensors.",
                 "/whereis": "Return exact GPS location of your clients",
                 "/takepic": "Return a picture taken from your RPI's webcam",
                 "/torrent": "Adds your torren into our torrent client.",
                 "/status": "Returns some important services' status as well as public RPI's IP address.",
                 "/random": "Select a command among all configured and possible commands",
                 "/help": "Returns help about all possible commands that are configured"
                 }


# COMMAND: /help
# COMMENT: RETURN all possible commands that are available.
# RETURN: String with commands and comments.
def command_help(args):
    output_message = "Here are all our configured commmands! Enjoy them!!\n"
    for command_key, comments in list_commands.items():
        output_message += command_key + "\t" + comments + "\n"
    return output_message


"""
    Handle function!
"""


# handle. finds and execute a command msg from client.
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].split()[0]    # we split text and take command value
    args = msg['text'].split()[1:]      # list of arguments - first element
    booting_time = time.time()          # TeleBot booting EPOCH time!

    # older messages will be deleted!
    if int(msg['date']) < int(booting_time):
        logging.info("Deleting old messages...")
        return

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1, 6))
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
    elif command == "/status":
        bot.sendMessage(chat_id,  command_status(args))
    elif command == '/random':
        r_command = random.choice(list(list_commands))
        bot.sendMessage(chat_id,  "We selected " + r_command)
        new_msg = msg
        new_msg['text'] = r_command
        bot.sendMessage(chat_id, handle(new_msg))
    elif command == "/help":
        bot.sendMessage(chat_id,  command_help(args))
    else:
        bot.sendMessage(chat_id, random.choice(command_not_found))
        bot.sendMessage(chat_id,  command_help(args))


"""
    Connecting to BoT!
"""
bot = telepot.Bot(variables.token_bot_api)

"""
    Bot is booted and welcome message!
"""
# Welcome message! we just started up!
bot.sendMessage(variables.bot_chat_id, random.choice(welcome_messages))

MessageLoop(bot, handle).run_as_thread()
logging.info('I am listening ...')

while 1:        # we keep program on and listening
    time.sleep(10)
