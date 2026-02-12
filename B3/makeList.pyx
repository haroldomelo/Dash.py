import pandas as pd
import MetaTrader5 as mt5
import datetime
import pytz
from .selStocks import *

def maxPrices():
    from .dadosB3 import getAllStocks  # Importa aqui para evitar circularidade
    acoes_df = getAllStocks()  # Chama getAllStocks e armazena o DataFrame
    df = getPrices(acoes_df)  # Passa o DataFrame para getPrices
    df = df[df['Ticker'].isin(acoes_df)]  # Filtra com base no índice do DataFrame acoes_df
    df = df.sort_values('Retorno', ascending=False)
    df = df.head(5)
    df = df.reset_index(drop=True)
    return df

def getPrices(tickersChoices, principal = False):
    mt5.initialize()    
    df_Price = pd.DataFrame(
                    columns = ['Ticker', 'Preço', 'Retorno', 'Data Fechamento']
                    , index = list(range(0, len(tickersChoices)))
                )
    
    for i, ticker in enumerate(tickersChoices):
        if principal == False: # Se não for principal, só mostre empresas com liquidez maior que 10 negociações ao dia
            if mt5.symbol_info(ticker).session_deals > 10:
                retorno = mt5.symbol_info(ticker).price_change
                fechamento = mt5.symbol_info(ticker).last
                data = mt5.symbol_info(ticker).time
                data = datetime.datetime.fromtimestamp(data, tz=pytz.timezone('Brazil/West'))
                
                df_Price.loc[i, :] = [ticker, fechamento, retorno, data] 

            else:
                retorno = mt5.symbol_info(ticker).price_change
                fechamento = mt5.symbol_info(ticker).last
                data = mt5.symbol_info(ticker).time
                data = datetime.datetime.fromtimestamp(data, tz=pytz.timezone('Brazil/West'))
                
                df_Price.loc[i, :] = [ticker, fechamento, retorno, data] 


    return df_Price

def makeList():
    # Cria uma lista com os dados da ação
    
    '''
        Vencimento do contrato do dólar acontece no primeiro dia útil do mês.
        Já o vencimento do contrato do índice ocorre a cada dois meses (apenas nos meses pares).
    '''

    legendaIndice = pd.Series(
                        [2, 4, 6, 8, 10, 12]
                        , index=['G', 'J', 'M', 'Q', 'V', 'Z']
                    )
    legendaDolar = pd.Series(
                        list(range(1, 13))
                        , index=['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
                    )
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    if month == 12:
        letra_Indice = 'G'
        letra_Dolar = 'F'
        cod_Indice = 'WIN' + letra_Indice + str(year + 1)[2:]
        cod_Dolar = 'WDO' + letra_Dolar + str(year + 1)[2:]
    else:
        letra_Indice = (legendaIndice[legendaIndice > month]).index[0]
        letra_Dolar = (legendaDolar[legendaDolar > month]).index[0]
        cod_Indice = 'WIN' + letra_Indice + str(year)[2:]
        cod_Dolar = 'WDO' + letra_Dolar + str(year)[2:]

    tickers_Juros = ['DI1F' + str(year_Choice)[2:] for year_Choice in range(year + 1, year + 6)]
    tickers_B3 = [cod_Indice, cod_Dolar, 'SMAL11', 'IVVB11'] + tickers_Juros

    return tickers_B3

def getTickers():
    acoes = get_Stocks()
    tickers_B3 = makeList(acoes)
    tickersTtl = acoes + tickers_B3

    for ticker in tickersTtl:
        mt5.symbol_select(ticker)

    # dadosB3 = select_Stocks(nota)
    # print(dadosB3)
    # dadosB3.to_csv(f"B3/{nota}.csv", index = False)
