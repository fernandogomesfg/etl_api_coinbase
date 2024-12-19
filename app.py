import requests

def get_coinbase_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    return response.json()

print(get_coinbase_data()['data'])
