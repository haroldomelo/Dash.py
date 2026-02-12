import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from io import StringIO
import time

def capturarDI(url, driver):
    """
    Captura tabelas de dados DI do site da BMF
    """
    """Captura as tabelas de DI do site da B3"""
    try:
        print(f"  Acessando URL...")
        driver.get(url)
        
        # Aguardar carregamento
        time.sleep(3)
        
        local_tabela = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[3]/table'
        local_indice = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[1]/table'
        
        print(f"  Aguardando elementos...")
        wait = WebDriverWait(driver, 10)
        
        # Tentar localizar elementos
        elemento = wait.until(EC.presence_of_element_located((By.XPATH, local_tabela)))
        elemento_ind = wait.until(EC.presence_of_element_located((By.XPATH, local_indice)))
        
        print(f"  Extraindo HTML...")
        htmlTab = elemento.get_attribute('outerHTML')
        html_ind = elemento_ind.get_attribute('outerHTML')
        
        print(f"  Convertendo para DataFrame...")
        tab = pd.read_html(htmlTab)[0]
        indTab = pd.read_html(html_ind)[0]
        
        print(f"  Tabela shape: {tab.shape}, Índice shape: {indTab.shape}")
        
        return tab, indTab
        
    except NoSuchElementException as e:
        print(f"  Elemento não encontrado: {e}")
        raise
        
    except TimeoutException as e:
        print(f"  Timeout ao aguardar elementos")
        raise
        
    except Exception as e:
        print(f"  Erro inesperado em capturarDI2: {e}")
        import traceback
        traceback.print_exc()
        return None, None