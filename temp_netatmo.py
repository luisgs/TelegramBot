import requests
import time
import json
import variables




def netatmo_grant_token():
    data = dict(grant_type = 'password', client_id = variables.netatmo_client_id,
            client_secret = variables.netatmo_client_secret,
            username = variables.netatmo_username, password = variables.netatmo_password,
            scope='read_thermostat')
    resp = requests.post('https://api.netatmo.com/oauth2/token', data=data,
                            verify=False)   # Ignore SSL certificate's verification
    return resp


def netatmo_homestatus():
    resp = netatmo_grant_token()
    if resp.status_code == 200:
        token = resp.json()
        token['expiry'] = int(time.time()) + token['expires_in']
        print("TOKEN: " + token['access_token'])
        resp = requests.get('https://api.netatmo.com/api/homesdata?access_token=' +
                                token['access_token'], verify=False)
        data = resp.json()
        print(json.dumps(data))
    else:
        print("There is an error")


def netatmo_room_temp():
    resp = netatmo_grant_token()
    if resp.status_code == 200:
        token = resp.json()
        token['expiry'] = int(time.time()) + token['expires_in']
        netatmo_headers = {'accept': 'application/json', 'Authorization' : 'Bearer {}'.format(token['access_token'])}
        params = {'home_id' : variables.netatmo_home_id}
        temp_int = requests.get('https://api.netatmo.com/api/homestatus', headers=netatmo_headers, params=params, verify=False).json()
        room_temp = temp_int['body']['home']['rooms'][0]['therm_measured_temperature']
        print(room_temp)
    else:
        print("There is an error")

netatmo_room_temp()
