
import sys, logging

error_import = False
try:
    error_import = True
    import Adafruit_DHT
except (ModuleNotFoundError, ImportError) as error:
    logging.exception("Import Adafruit_DHT has failed! %s", error)


# Logging as output logging messages.
# logging.basicConfig(stream=sys.stderr, level=logging.INFO)

"""
    FUNCTION to return temp and humidity from TWO sensors in OUR RPI
"""

# list of pins used for DHT sensor
list_DHT_PIN = [4, 17]

def return_DHT_sensor_info(DHT_PIN):
    DHT_SENSOR = Adafruit_DHT.DHT22
    hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return hum, temp

def return_ALL_DHT_temp_humid():
    list_dht_values = []
    if error_import:
        return list_dht_values
    else:
        for index, DHT_PIN in enumerate(list_DHT_PIN):
            hum, temp = return_DHT_sensor_info(DHT_PIN)
            if ((hum is not None) and (temp is not None)):
                logging.info("{0}: Temp_{0}={1:0.1f}*C  Humidity_{0}={2:0.1f}%".format(index, temp, hum))
            else:
                logging.error("Failed to retrieve data from humidity sensor")
        return list_dht_values


"""
humidity_1, temperature_1 = 0, 0
humidity_2, temperature_2 = 0, 0

if not error_import:
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN_1 = 4   # sensor 1
    DHT_PIN_2 = 17  # sensor 2

    humidity_1, temperature_1 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_1)
    humidity_2, temperature_2 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_2)

def temp():
    if (humidity_1 is not None and
        temperature_1 is not None and
            humidity_2 is not None and
                temperature_2 is not None):
        logging.info("1: Temp_1={0:0.1f}*C  Humidity_1={1:0.1f}%".format(temperature_1, humidity_1))
        logging.info("2: Temp_2={0:0.1f}*C  Humidity_2={1:0.1f}%".format(temperature_2, humidity_2))
        temp_humidity = [[temperature_1,humidity_1], [temperature_2, humidity_2]]
    else:
        logging.error("Failed to retrieve data from humidity sensor")
        temp_humidity = ()

    return temp_humidity
"""
