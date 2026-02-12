import pandas as pd
import MetaTrader5 as mt5
import datetime
import pytz
# from .selStocks import *
# from .makeList import *

def getAllStocks():
# def getAllStocks(nota):
    mt5.initialize()

    symbols = mt5.symbols_get()
    # symbols
    
    tickers = [symbol.name for symbol in symbols] # forma abreviada do for loop
    tickers = sorted(tickers, reverse = True)
    # tickers

    acoes = []
    dadosB3 = []
    for ticker in tickers:
        try:
            int(ticker[3]) # quarto caracter tem que ser uma string, não um número
        except:
            fticker = ticker[4:]

            if mt5.symbol_info(ticker).session_deals > 100: # Só mostre empresas com liquidez maior que 10 negociações ao dia
                if len(fticker) == 2:
                    if fticker == "11": #para tickers que possuem final 11, substitui e adiciona a série 3 ou 4 para pesquisar dados.
                        if (ticker[0:4] + "3") in acoes or (ticker[0:4] + "4") in acoes:
                            acoes.append(ticker)
                            
                if len(fticker) == 1:
                    if fticker == "3" or fticker == "4":
                        acoes.append(ticker)
    
    # encerrar o meda trader 5, para não consumir memória a toa
    mt5.shutdown()

    # # transforma a lista de ações em um DataFrame
    # acoes = pd.DataFrame(acoes, columns=['Ticker'])
    # acoes = acoes.set_index(['Ticker'])
    # acoes = acoes.drop_duplicates()
    # acoes = acoes.sort_index()

    # print(acoes, len(acoes))
    return sorted(acoes, reverse=False) # retorna uma lista