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
        # print(response.text)
        rate = json_response.get('rate')
        return rate
    else:
        print('Algo no ha ido bien. Error ',
              response.status_code, response.reason)


def consultar_inversion():
    # modificar según SQL invertido
    endpoint = '/v1/assets?filter_asset_id=EUR;BTC;ETH;USDT;ADA;SOL;XRP;DOT;DOGE;SHIB'
    url = server + endpoint
    headers = {
        'X-CoinAPI-Key': apikey
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_response = response.json()

        for coin in json_response:
            id = coin.get('asset_id')
            # if (id in ['BTC', 'USD', 'EUR', 'ETH']):
            #     print(id, '-', coin.get('name'), coin.get('type_is_crypto'))
            print(id, '-', coin.get('name'), '-',
                  coin.get('price_usd'), '-', coin.get('time'))
    else:
        print('Algo no ha ido bien. Error ',
              response.status_code, response.reason)


# consultar_cambio('EUR', 'USD')
