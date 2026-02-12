import pandas as pd
from selenium import webdriver
import time
import datetime  # Alterado: agora importa o módulo datetime
from datetime import timedelta, date  # Mantido para timedelta e date
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dateutil.parser import parse
from .tratarDI import *
from .capturarDI import *

def webScrapingDI():
    hoje = datetime.datetime.now()
    umAnoAtras = hoje - timedelta(days=365)
    tresAnosAtras = hoje - timedelta(days=365*3)
    cincoAnosAtras = hoje - timedelta(days=365*5)
    dezAnosAtras = hoje - timedelta(days=365*10)
    lstDatas = [hoje, umAnoAtras, tresAnosAtras, cincoAnosAtras, dezAnosAtras]
    lstNames = ['hoje', 'um_ano_atras', 'tres_anos_atras', 'cinco_anos_atras', 'dez_anos_atras']
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        data_di = date(2023, 10, 18)
        data_di_str = data_di.strftime('%d/%m/%Y')
        
        # URL formatada corretamente (sem quebras de linha)
        url = f"https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&Data={data_di_str}&Mercadoria=DI1"
        
        driver.get(url)
        
        # Aguardar o carregamento da página
        wait = WebDriverWait(driver, 10)
        
        local_tabela = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[3]/table'
        local_indice = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[1]/table'  
        
        # Usar By.XPATH e esperar o elemento estar presente
        elemento = wait.until(EC.presence_of_element_located((By.XPATH, local_tabela)))
        elemento_ind = wait.until(EC.presence_of_element_located((By.XPATH, local_indice)))
        
        htmlTab = elemento.get_attribute('outerHTML')
        html_ind = elemento_ind.get_attribute('outerHTML')
        
        tab = pd.read_html(htmlTab)[0]
        indTab = pd.read_html(html_ind)[0]
        
        legenda = pd.Series(
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            index=['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
        )
        
        tab.columns = tab.loc[0]
        tab = tab['ÚLT. PREÇO']
        # print(tab)
        tab = tab.drop(0, axis=0) # exclui a primeira linha da primeira coluna que virou header
        # print(tab)
        
        indTab.columns = indTab.loc[0]
        indTab = indTab.drop(0, axis=0)
        print(indTab)
        
        tab.index = indTab['VENCTO'] # troca o index pela coluna VENCTO do indTab
        tab = tab.astype(int)
        tab = tab[tab != 0]
        tab = tab/1000
        # print(tab)
        
        lstDados = []
        for ind in tab.index:
            letra = ind[0]
            ano = ind[1:3]
            mes = legenda[letra]
            dataStr = f"{mes}-{ano}"
            print(dataStr)
            # dataStr = datetime.strptime(dataStr, "%b-%y")
            # dataStr = dataStr.strptime('%Y-%m-%d')
            # dataStr = parse(dataStr)
            # dataStr = datetime.datetime.strptime(dataStr, "%b-%y").strftime("%b-%y")
            dataStr = datetime.datetime.strptime(dataStr, "%b-%y")  # Corrigido: usa datetime.datetime.strptime
            lstDados.append(dataStr)
        
        # print(f'Lista de dados {lstDados}')
        # print(f'Tabela {tab}')
        tab.index = lstDados
        tab = tab/100

        print(f'Tipo da variável tab: {type(tab)}')
        # isinstance(tab, pd.Series) # Retorna True se for Series.
        # isinstance(tab, pd.DataFrame) # Retorna False se for DataFrame.
        if isinstance(tab, pd.Series) == True:
            print("tab é uma Serie")
        elif isinstance(tab, pd.DataFrame) == True:
            print("tab é uma DataFrame")
        else:
            print("tab não é uma Series nem DataFrame")

        # print(tab.columns) # Removido: tab é uma Series, não tem .columns
        # print(tab.index)
        # print(tab)
        
        return tab
        
    except Exception as e:
        print(f"Erro: {e}")
        raise
    finally:
        driver.quit()