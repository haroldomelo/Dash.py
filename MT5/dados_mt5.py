import pandas as pd
from selenium import webdriver
import os
import time
import datetime
from datetime import timedelta, date
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dateutil.parser import parse
import pandas as pd
import MetaTrader5 as mt5
import pytz

def dadosMT5():

    mt5.initialize()

    symbols = mt5.symbols_get()
    # symbols
    
    tickers = [symbol.name for symbol in symbols] # forma abreviada do for loop
    tickers = sorted(tickers, reverse = True)
    # print(tickers)
    # print(len(tickers))

    acoes = []
    for ticker in tickers:
        try:
            int(ticker[3]) # quarto caracter tem que ser uma string, não um número
        except:
            fticker = ticker[4:]
            if len(fticker) == 2:
                if fticker == "11": #para tickers que possuem final 11, substitui e adiciona a série 3 ou 4 para pesquisar dados.
                    if (ticker[0:4] + "3") in acoes or (ticker[0:4] + "4") in acoes:
                        acoes.append(ticker)
                        
            if len(fticker) == 1:
                if fticker == "3" or fticker == "4":
                    acoes.append(ticker)
    
    if acoes:
        
        os.makedirs('MT5/files/', exist_ok=True)
        acoes = pd.DataFrame(acoes)
        acoes.to_csv('MT5/files/MT5.csv', index=False)
        acoes.to_parquet('MT5/files/MT5.parquet', index=False)

        return acoes
    else:
        print("\n✗ Nenhum dado foi capturado.")
        return None

def makeListMT5():
    # Lista de contratos de dólar
    lstLegInd = pd.Series([2, 4, 6, 8, 10, 12]
                        , index = ['G', 'J', 'M', 'Q', 'V', 'Z'])
    lstLegDolar = pd.Series(list(range(1, 13))
                        , index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])
    # F = Janeiro, G = Fevereiro, H = Março, J = Abril, K = Maio, M = Junho,
    # N = Julho, Q = Agosto, U = Setembro, V = Outubro, X = Novembro, Z = Dezembro
    ano = datetime.datetime.now().year
    mes = datetime.datetime.now().month

    if mes == 12:
        letraInd = 'G'
        letraDolar = 'F'
        codInd = 'WIN' + letraInd + str(ano)[2:]
        codDolar = 'WDO' + letraDolar + str(ano)[2:]
    else:
        letraInd = (lstLegInd[lstLegInd >= mes]).index[0]
        letraDolar = (lstLegDolar[lstLegDolar >= mes]).index[0]
        codInd = 'WIN' + letraInd + str(ano)[2:]
        codDolar = 'WDO' + letraDolar + str(ano)[2:]

    tickerJuros = ['DI1F' + str(anoEscolhido)[2:] for anoEscolhido in range(ano+1, ano + 6)]
    tickerMercado = [codInd, codDolar, 'SMALL11', 'IVVB11'] + tickerJuros

    return tickerMercado

def selectMT5():
    acoes = dadosMT5()
    '''
        O vencimento do contrato de dólar acontece no primeiro dia útil do mês.
        Já o vencimento do contrato de índice acontece a cada dois  meses (somente nos meses pares).
    '''
    tickersMT5 = makeListMT5()
    tickersTTL = acoes + tickersMT5

    for ticker in tickersTTL:
        mt5.symbol_select(ticker, True)

def capturarMT5(selectTicker, principal = False):
    
    mt5.initialize()
    dfCotacoes = pd.DataFrame(columns=['Date', 'Ticker', 'Preço', 'Retorno']
                              , index = list(range(0, len(selectTicker))))
    for i, ticker in enumerate(selectTicker):
        if principal == False:
            if mt5.symbol_info(ticker).session_deals > 10:
                retorno = mt5.symbol_info(ticker).price_change
                fechamento = mt5.symbol_info(ticker).last
                dfCotacoes.loc[i, :] = [datetime.datetime.now().strftime('%Y-%m-%d'), ticker, fechamento, retorno]
        else:
            retorno = mt5.symbol_info(ticker).price_change
            fechamento = mt5.symbol_info(ticker).last
            dfCotacoes.loc[i, :] = [datetime.datetime.now().strftime('%Y-%m-%d'), ticker, fechamento, retorno]
    
    dfCotacoes.to_csv('MT5/files/cotacoes.csv', index = False)
    dfCotacoes.to_parquet('MT5/files/cotacoes.parquet', index = False)
    return dfCotacoes

def maioresAltas(tickersIbov):
    acoes = dadosMT5()
    df = capturarMT5(acoes)
    df = df[df['Ticker'].isin(tickersIbov)]
    df = df.sort_values(by='Retorno', ascending=False)
    df = df.head(3)
    df = df.reset_index(drop=True)
    return df

def maioresBaixas(tickersIbov):
    acoes = dadosMT5()
    df = capturarMT5(acoes)
    df = df[df['Ticker'].isin(tickersIbov)]
    df = df.sort_values(by='Retorno', ascending=True)
    df = df.head(3)
    df = df.reset_index(drop=True)
    return df

def histoicoMT5():
    mt5.initialize()
    acoes = dadosMT5()
    lstCotacoes = []
    timezone = pytz.timezone("Brazil/West")
    dataIni = (datetime.datetime.now(tz = timezone) - datetime.timedelta(days = 1095))
    dataFin = datetime.datetime.now(tz = timezone)

    for acao in acoes:
        try:
            cotacoes = mt5.copy_rates_range(acao, mt5.TIMEFRAME_D1, dataIni, dataFin)
            cotacoes = pd.DataFrame(cotacoes)
            
            cotacoes = cotacoes[['time', 'open', 'high', 'low', 'close']]
            cotacoes['time'] = pd.to_datetime(cotacoes['time'], unit = 's')
            cotacoes['ticker'] = acao
        except:
            print(acoes)
        lstCotacoes.append(cotacoes)
    dfCotacoes = pd.concat(lstCotacoes, ignore_index = True)
    empresas = dfCotacoes['ticker'].unique().tolist()
    dfEmpresas = pd.DataFrame({'ticker': empresas})
    dfEmpresas.to_csv('MT5/files/tickers.csv', index = False)
    dfEmpresas.to_parquet('MT5/files/tickers.parquet', index = False)