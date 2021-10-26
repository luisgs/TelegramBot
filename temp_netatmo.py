import requests
import time
import json
import variables


data = dict(grant_type = 'password', client_id = variables.netatmo_client_id,
        client_secret = variables.netatmo_client_secret,
        username = variables.netatmo_username, password = variables.netatmo_password,
        scope='read_thermostat')

resp = requests.post('https://api.netatmo.com/oauth2/token', data=data,
                        verify=False)   # Ignore SSL certificate's verification

if resp.status_code == 200:
    token = resp.json()
    token['expiry'] = int(time.time()) + token['expires_in']
    print(token['access_token'])
    resp = requests.get('https://api.netatmo.com/api/homesdata?access_token=' +
                            token['access_token'], verify=False)
    data = resp.json()
    print(json.dumps(data))
else:
    print("There is an error")
