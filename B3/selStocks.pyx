import pandas as pd
import MetaTrader5 as mt5
import datetime
import pytz
from .dadosB3 import *
from .makeList import *

def select_Stocks(nota):
    # cotação atual
    ticker = nota #'WEGE3
    retorno = mt5.symbol_info(ticker).price_change
    fechamento = mt5.symbol_info(ticker).last

    print(retorno, fechamento)

    # histórico de cotações
    acao = nota
    timezone = pytz.timezone('Brazil/West')
    dataIni = (datetime.datetime.now(tz = timezone) - datetime.timedelta(days = 1095))
    dataFin = datetime.datetime.now(tz = timezone)

    cotacoes = mt5.copy_rates_range(acao, mt5.TIMEFRAME_D1, dataIni, dataFin)
    cotacoes = pd.DataFrame(cotacoes)
    cotacoes = cotacoes[['time', 'open', 'high', 'low', 'close']]
    cotacoes['time'] = pd.to_datetime(cotacoes['time'], unit = 's')
    cotacoes['ticker'] = acao

    return cotacoes