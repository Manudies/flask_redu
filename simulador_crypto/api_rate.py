import requests
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('APIKEY')
origen = '/EUR'
destino = '/USD'
server = 'https://rest.coinapi.io'
endpointrate = '/v1/exchangerate' + origen + destino
url2 = server + endpointrate
payload = {}
headers = {
    'Accept': 'text/json',
    'X-CoinAPI-Key': apikey
}

response = requests.request("GET", url2, headers=headers, data=payload)
json_response = response.json()
if response.status_code == 200:
    # print(response.text)
    time = json_response.get('time')
    rate = json_response.get('rate')
    print(time, '-', rate)
else:
    print('Algo no ha ido bien. Error ', response.status_code, response.reason)
