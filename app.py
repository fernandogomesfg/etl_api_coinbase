# Importando bibliotecas
import time
import requests
from datetime import datetime


# Função para obter os dados da API Coinbase
def get_coinbase_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    return response.json()


# Função para transformar os dados da API Coinbase
def transform_coinbase_data(data):
    valor = data['data']['amount']
    criptomoeda = data['data']['base']
    moeda = data['data']['currency']
    timestamp = datetime.now().timestamp()

    # Criando um dicionário com os dados transformados
    dados_transformados = {
        'valor': valor,
        'criptomoeda': criptomoeda,
        'moeda': moeda,
        'timestamp': timestamp
    }

    return dados_transformados





if __name__ == "__main__":
    while True:
        dados_json = get_coinbase_data()
        dados_transformados = transform_coinbase_data(dados_json)
        print(dados_transformados)
        time.sleep(15)
    
    
