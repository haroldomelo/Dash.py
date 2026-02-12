import requests
import pandas as pd
from bcb import sgs
from datetime import timedelta, datetime
import os

def inflacao():
    hoje = datetime.now()
    inicio = hoje - timedelta(days=4000)

    inflacao = None
    while inflacao is None:
        inflacao = sgs.get({'ipca': 433
                            ,'igp-m': 189}
                            ,start=inicio)
    inflacao = inflacao/100
    # Exportar dados tratados
    os.makedirs('B3/files/', exist_ok=True)  # Cria o diretório se não existir
    inflacao.to_csv('B3/files/inflacao.csv')
    inflacao.to_parquet('B3/files/inflacao.parquet', index=False)

def attDividaPIB():
    hoje = datetime.now()
    anoPassado = hoje.year - 1
    umAnoAtras = hoje - timedelta(days=4000)
    dados = None
    
    while isinstance(dados, pd.DataFrame) == False:
        dados = sgs.get({'Dívida_PIB': 13762},start=umAnoAtras)
    dados = dados/100

    # Exportar dados tratados
    os.makedirs('B3/files/', exist_ok=True)  # Cria o diretório se não existir
    dados.to_csv('B3/files/divida_pib.csv')
    dados.to_parquet('B3/files/divida_pib.parquet', index=False)

def att_dolar():
    hoje = datetime.now()
    inicio = hoje - timedelta(days=4000)
    dados = None
    
    #tentar dar get no bacen, se der erro, tentar de novo. O isinstance é para verificar se o dado retornado é um dataframe,
    #se não for, é porque deu erro e tem que tentar de novo. Ele serve para comparar as variáveis, neste caso,
    #verificando se a variável retorna um dataframe.
    while isinstance(dados, pd.DataFrame) == False: 
        dados = sgs.get({'DOLAR': 1},start=inicio)
    
    # Exportar dados tratados
    os.makedirs('B3/files/', exist_ok=True)  # Cria o diretório se não existir
    dados.to_csv('B3/files/dolar.csv')
    dados.to_parquet('B3/files/dolar.parquet', index=False)