# Importando bibliotecas
import time
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, BitcoinPreco

# Carrega variaveis de ambiente do arquivo .env
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

Database_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(Database_URL)
Session = sessionmaker(bind=engine)

# Funcao para criar a tabela no banco de dados
def create_table():
    Base.metadata.create_all(engine)
    print("Tabela criada com sucesso!")

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
    timestamp = datetime.now()

    # Criando um dicionário com os dados transformados
    dados_transformados = {
        'valor': valor,
        'criptomoeda': criptomoeda,
        'moeda': moeda,
        'timestamp': timestamp
    }

    return dados_transformados

# funcao para salvar os dados no banco de dados
def save_data(dados):
    session = Session()
    novo_registro = BitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos com sucesso!")
    
    print("Dados salvos com sucesso!")



if __name__ == "__main__":
    create_table()
    print("Iniciando a coleta de dados com actualizacao de 15 segundos...")

    while True:
        try:
            dados_json = get_coinbase_data()
            if dados_json:
                dados_transformados = transform_coinbase_data(dados_json)
                print("Dados Transformados: ", dados_transformados)
                save_data(dados_transformados)
            time.sleep(15)
        except KeyboardInterrupt:
            print("Saindo do programa...")
            break
        except Exception as e:
            print(f"Erro ao coletar os dados: {e}")
            time.sleep(15)
    
    
