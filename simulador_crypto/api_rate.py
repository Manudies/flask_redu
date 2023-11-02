import requests
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('APIKEY')
server = 'https://rest.coinapi.io'

# Función de consulta de cambio entre dos monedas


def consultar_cambio(origen, destino):
    endpoint = f'/v1/exchangerate/{origen}/{destino}'
    url = server + endpoint
    payload = {}
    headers = {
        'Accept': 'text/json',
        'X-CoinAPI-Key': apikey
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()
    if response.status_code == 200:
        rate = json_response.get('rate')
        return rate
    else:
        print('Algo no ha ido bien. Error ',
              response.status_code, response.reason)


# Consulta de monedas para estado de la inversión
def consultar_inversion():
    endpoint = '/v1/exchangerate/EUR?filter_asset_id=BTC;ETH;USDT;ADA;SOL;XRP;DOT;DOGE;SHIB'
    url = server+endpoint
    payload = {}
    headers = {
        'Accept': 'text/json',
        'X-CoinAPI-Key': apikey
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        json_response = response.json()
        rate = json_response["rates"]
        indice = 0
        rates = []
        for i in rate:
            rates.append(rate[indice]['rate'])
            indice += 1
        return rates

    else:
        print('Algo no ha ido bien. Error ',
              response.status_code, response.reason)
