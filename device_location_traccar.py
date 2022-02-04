"""Example usage of pytraccar."""
import asyncio
import aiohttp
from pytraccar.api import API
import sys
import logging
# all our PERSONAL variables are stored in here
import variables

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


HOST = variables.traccar_host
PORT = variables.traccar_port
USERNAME = variables.traccar_username
PASSWORD = variables.traccar_password

device = variables.traccar_mydevice
latitude, longitude = 0, 0


def device_lat_long(mydevice):
    async def test():
        """Example usage of pytraccar."""
        async with aiohttp.ClientSession() as session:
            data = API(LOOP, session, USERNAME, PASSWORD, HOST, PORT)
            global latitude, longitude
            await data.get_device_info()
            await data.get_events([2])

            logging.info("Device_info:" + str(data.device_info))
            logging.info("Positions:" + str(data.positions))
            logging.info("Devices:" + str(data.devices))
            logging.info("Geofences:" + str(data.geofences))
            logging.info("Events:" + str(data.events))

            if mydevice in data.device_info:
                latitude = data.device_info[mydevice]['latitude']
                longitude = data.device_info[mydevice]['longitude']

    LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(LOOP)
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(test())
    logging.info("Device latitude: " + (str(latitude)))
    logging.info("Device longitude: " + (str(longitude)))

    return latitude, longitude


print("This are some values" + str(device_lat_long(device)))
