import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import datetime
import plotly.graph_objects as go
from selenium.common.exceptions import NoSuchElementException
from DI.dadosDI import *
from B3.dadosB3 import *
# from B3.makeList import *
# from B3.bdHistory import *
from B3.setoresB3 import *
from B3.dadosBacen import *
from MT5.dados_mt5 import *

if __name__ == "__main__":

    # dados_b3 = getAllStocks()
    # print(dados_b3)
    
    # max_prices = maxPrices()
    # print(max_prices)
    
    # bd = bdHistory()
    # print(bd)
    
    setores_b3 = setorB3()
    print(setores_b3)

    # dados_di = webScrapingDI()
    # print(dados_di)

    mt5 = dadosMT5()
    # print(mt5)

    stocks = capturarMT5(selectTicker=['VALE3', 'WEGE3', 'PETR4', 'ITUB4'])
    print(stocks)

    histoicoMT5()

    inflacao()
    attDividaPIB()
    att_dolar()

    # dados_b3 = getAllStocks('BBAS3')
    # print(dados_b3)

    # dados_b3 = getPrices(['WEGE3', 'VALE3', 'BBAS3'])
    # print(dados_b3)

