
import sys, logging
import Adafruit_DHT


"""
    FUNCTION to return temp and humidity from TWO sensors in OUR RPI
"""
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
