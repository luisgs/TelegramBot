import requests
import time
import json
import variables
import sys, logging

# Logging as output logging messages.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Client credentials grant type
# https://api.netatmo.com/oauth2/token
def netatmo_grant_token():
    data = dict(grant_type = 'password', client_id = variables.netatmo_client_id,
            client_secret = variables.netatmo_client_secret,
            username = variables.netatmo_username, password = variables.netatmo_password,
            scope='read_thermostat')
    resp = requests.post('https://api.netatmo.com/oauth2/token', data=data,
                            verify=False)   # Ignore SSL certificate's verification
    return resp

# Get current status of a home and devices
# https://api.netatmo.com/api/homesdata
def netatmo_homestatus():
    resp = netatmo_grant_token()
    if resp.status_code == 200:
        token = resp.json()
        token['expiry'] = int(time.time()) + token['expires_in']
        logging.debug("TOKEN: " + token['access_token'])
        resp = requests.get('https://api.netatmo.com/api/homesdata?access_token=' +
                                token['access_token'], verify=False)
        data = resp.json()
        #print(json.dumps(data))
        return json.dumps(data)
    else:
        logging.info("There is an error")

# retrieve data of a devices
# https://api.netatmo.com/api/homestatus
def netatmo_room_temp():
    resp = netatmo_grant_token()
    if resp.status_code == 200:
        token = resp.json()
        token['expiry'] = int(time.time()) + token['expires_in']
        netatmo_headers = {'accept': 'application/json', 'Authorization' : 'Bearer {}'.format(token['access_token'])}
        params = {'home_id' : variables.netatmo_home_id}
        temp_int = requests.get('https://api.netatmo.com/api/homestatus', headers=netatmo_headers, params=params, verify=False).json()
        room_temp = temp_int['body']['home']['rooms'][0]['therm_measured_temperature']
        return room_temp
    else:
        logging.info("There is an error")

logging.info("Netatmo: room Temp is: " + str(netatmo_room_temp()))
