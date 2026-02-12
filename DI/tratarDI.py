import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time 
import datetime
import plotly.graph_objects as go
from selenium.common.exceptions import NoSuchElementException

# Método para tratar os dados
def tratarDI(tab, indTab):
    """Trata os dados das tabelas de DI"""
    try:
        # Validar inputs
        if tab is None or indTab is None:
            print("  ✗ Erro: tabela ou índice é None")
            return None
        
        print(f"  Tratando dados...")
        
        # Configurar colunas
        tab.columns = tab.loc[0]
        tab = tab['ÚLT. PREÇO']
        tab = tab.drop(0, axis=0)
        
        indTab.columns = indTab.loc[0]
        indTab = indTab.drop(0, axis=0)
        
        # Processar valores
        tab.index = indTab['VENCTO']
        tab = tab.astype(float)
        tab = tab[tab != 0]
        tab = tab / 1000
        
        # Converter códigos de vencimento para datas
        legenda = pd.Series(
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            index=['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
        )
        
        lstDados = []
        for ind in tab.index:
            letra = ind[0]
            ano = ind[1:3]
            mes = legenda[letra]
            dataStr = f"{mes}-{ano}"
            dataFormatada = datetime.datetime.strptime(dataStr, "%b-%y")
            lstDados.append(dataFormatada)
        
        tab.index = lstDados
        # tab = tab / 100
        
        print(f"  ✓ Tratamento concluído: {len(tab)} registros")
        
        return tab
        
    except Exception as e:
        print(f"  ✗ Erro em tratarDI2: {e}")
        import traceback
        traceback.print_exc()
        return None	