import pandas as pd
import MetaTrader5 as mt5
import datetime
import pytz
import os
from .selStocks import *
from .makeList import *

def bdHistory():

    from .dadosB3 import getAllStocks  # Importa aqui para evitar circularidade
    acoes = getAllStocks()
    
    if not mt5.initialize():
        print("Falha ao inicializar o MetaTrader 5")
        return

    lsCotacoes = []
    timezone = pytz.timezone('Brazil/West')
    dataIni = (datetime.datetime.now(tz = timezone) - datetime.timedelta(days = 1095))
    dataFin = datetime.datetime.now(tz = timezone)

    for acao in acoes:
        try:
            cotacoes = mt5.copy_rates_range(acao, mt5.TIMEFRAME_D1, dataIni, dataFin)
            cotacoes = pd.DataFrame(cotacoes)
            cotacoes['time'] = pd.to_datetime(cotacoes['time'], unit='s')
            cotacoes['ticker'] = acao  # Adiciona a coluna 'ticker'
            lsCotacoes.append(cotacoes)
        except Exception as e:
            print(f"Erro ao obter dados para {acao}: {e}")
            continue  # Continua para a próxima ação

    if lsCotacoes:
        cotFn = pd.concat(lsCotacoes)
        print(cotFn.head())  # Mostra as primeiras linhas do DataFrame
        if 'ticker' in cotFn.columns:
            empresas = cotFn['ticker'].unique()
            df_empresas = pd.DataFrame({'tickers': empresas})

            os.makedirs('B3', exist_ok=True)  # Cria o diretório se não existir
            df_empresas.to_csv('B3/tickers.csv', index=False)
            cotFn.to_parquet('B3/cotacoes.parquet', index=False)
        else:
            print("A coluna 'ticker' não existe no DataFrame.")
    else:
        print("Nenhuma cotação foi coletada.")