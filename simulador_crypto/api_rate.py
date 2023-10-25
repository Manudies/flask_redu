import requests
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('APIKEY')
server = 'https://rest.coinapi.io'


def consultar_cambio(origen, destino):
    endpoint = f"/v1/exchangerate/{origen}/{destino}"
    url = server + endpoint
    payload = {}
    headers = {
        'Accept': 'text/json',
        'X-CoinAPI-Key': apikey
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()
    if response.status_code == 200:
        print(response.text)
        time = json_response.get('time')
        rate = json_response.get('rate')
        print(time, '-', rate)
        return time, rate
    else:
        print('Algo no ha ido bien. Error ',
              response.status_code, response.reason)


def consultar_inversion():
    pass
