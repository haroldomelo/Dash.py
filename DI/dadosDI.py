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
from DI.capturarDI import *
from DI.tratarDI import *

def webScrapingDI():
    hoje = datetime.datetime.now()
    umMesAtras = hoje - timedelta(days=30)
    umAnoAtras = hoje - timedelta(days=365)
    tresAnosAtras = hoje - timedelta(days=365*3)
    cincoAnosAtras = hoje - timedelta(days=365*5)
    dezAnosAtras = hoje - timedelta(days=365*10)
    lstDatas = [hoje, umMesAtras, umAnoAtras, tresAnosAtras, cincoAnosAtras, dezAnosAtras]
    lstNames = ['Hoje', 'Há 1 mês', 'Há 1 ano', 'Há 3 anos', 'Há 5 anos', 'Há 10 anos']
    
    lstDFs = []
    
    for n, data in enumerate(lstDatas):
        print(f"\n{'='*50}")
        print(f"Processando: {lstNames[n]}")
        print(f"{'='*50}")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        data_di = data
        
        tabela = None
        indice = None
        sucesso = False
        
        try:
            for i in range(0, 1):
                data_di_str = data_di.strftime('%d/%m/%Y')
                print(f"\nTentativa {i+1}/1 - Data: {data_di_str}")
                
                # URL sem quebras de linha
                url = f"https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&Data={data_di_str}&Mercadoria=DI1"
                
                try:
                    tabela, indice = capturarDI(url, driver)
                    # tabela, indice = capturarDI2(url, driver)
                    
                    # Verificar se os dados foram capturados
                    if tabela is not None and indice is not None:
                        print(f"✓ Dados capturados com sucesso! `{data_di_str}`")
                        sucesso = True
                        break
                    else:
                        print(f"✗ Dados não encontrados (None retornado)")
                        data_di -= timedelta(days=1)
                        print(f"  Ajustando data para: {(data_di).strftime('%d/%m/%Y')}")
                        
                except (NoSuchElementException, TimeoutException) as e:
                    print(f"✗ Erro ao capturar: {type(e).__name__}")
                    data_di -= timedelta(days=1)
                    
                except Exception as e:
                    print(f"✗ Erro inesperado: {e}")
                    data_di -= timedelta(days=1)
            
            # Processar dados apenas se capturados com sucesso
            if sucesso and tabela is not None and indice is not None:
                print(f"\nProcessando dados...")
                print(f"Tipo tabela: {type(tabela)}")
                print(f"Tipo indice: {type(indice)}")
                
                # dfDI = tratarDI2(tabela, indice)
                dfDI = tratarDI(tabela, indice)
                
                if dfDI is not None and len(dfDI) > 0:
                    dfDI = dfDI.reset_index()
                    dfDI.columns = ['dt_Venc.', 'Preço']
                    dfDI['Período'] = lstNames[n]
                    lstDFs.append(dfDI)
                    print(f"✓ {len(dfDI)} registros adicionados")
                else:
                    print(f"✗ DataFrame vazio após tratamento")
            else:
                print(f"✗ Não foi possível capturar dados para {lstNames[n]}")
        
        except Exception as e:
            print(f"✗ Erro ao processar {lstNames[n]}: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            driver.quit()
    
    # Concatenar e exportar
    if lstDFs:
        dfDI_final = pd.concat(lstDFs, ignore_index=True)
        
        os.makedirs('DI/files/', exist_ok=True)
        dfDI_final.to_csv('DI/files/DI.csv', index=False)
        dfDI_final.to_parquet('DI/files/DI.parquet', index=False)
        
        print(f"\n{'='*50}")
        print(f"✓ Dados exportados com sucesso!")
        print(f"Total de registros: {len(dfDI_final)}")
        print(f"{'='*50}")
        
        return dfDI_final
    else:
        print("\n✗ Nenhum dado foi capturado.")
        return None


# def capturarDI2(url, driver):
#     """Captura as tabelas de DI do site da B3"""
#     try:
#         print(f"  Acessando URL...")
#         driver.get(url)
        
#         # Aguardar carregamento
#         time.sleep(3)
        
#         local_tabela = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[3]/table'
#         local_indice = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[1]/table'
        
#         print(f"  Aguardando elementos...")
#         wait = WebDriverWait(driver, 10)
        
#         # Tentar localizar elementos
#         elemento = wait.until(EC.presence_of_element_located((By.XPATH, local_tabela)))
#         elemento_ind = wait.until(EC.presence_of_element_located((By.XPATH, local_indice)))
        
#         print(f"  Extraindo HTML...")
#         htmlTab = elemento.get_attribute('outerHTML')
#         html_ind = elemento_ind.get_attribute('outerHTML')
        
#         print(f"  Convertendo para DataFrame...")
#         tab = pd.read_html(htmlTab)[0]
#         indTab = pd.read_html(html_ind)[0]
        
#         print(f"  Tabela shape: {tab.shape}, Índice shape: {indTab.shape}")
        
#         return tab, indTab
        
#     except NoSuchElementException as e:
#         print(f"  Elemento não encontrado: {e}")
#         raise
        
#     except TimeoutException as e:
#         print(f"  Timeout ao aguardar elementos")
#         raise
        
#     except Exception as e:
#         print(f"  Erro inesperado em capturarDI2: {e}")
#         import traceback
#         traceback.print_exc()
#         return None, None


# def tratarDI2(tab, indTab):
#     """Trata os dados das tabelas de DI"""
#     try:
#         # Validar inputs
#         if tab is None or indTab is None:
#             print("  ✗ Erro: tabela ou índice é None")
#             return None
        
#         print(f"  Tratando dados...")
        
#         # Configurar colunas
#         tab.columns = tab.loc[0]
#         tab = tab['ÚLT. PREÇO']
#         tab = tab.drop(0, axis=0)
        
#         indTab.columns = indTab.loc[0]
#         indTab = indTab.drop(0, axis=0)
        
#         # Processar valores
#         tab.index = indTab['VENCTO']
#         tab = tab.astype(float)
#         tab = tab[tab != 0]
#         tab = tab / 1000
        
#         # Converter códigos de vencimento para datas
#         legenda = pd.Series(
#             ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
#             index=['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
#         )
        
#         lstDados = []
#         for ind in tab.index:
#             letra = ind[0]
#             ano = ind[1:3]
#             mes = legenda[letra]
#             dataStr = f"{mes}-{ano}"
#             dataFormatada = datetime.datetime.strptime(dataStr, "%b-%y")
#             lstDados.append(dataFormatada)
        
#         tab.index = lstDados
#         # tab = tab / 100
        
#         print(f"  ✓ Tratamento concluído: {len(tab)} registros")
        
#         return tab
        
#     except Exception as e:
#         print(f"  ✗ Erro em tratarDI2: {e}")
#         import traceback
#         traceback.print_exc()
#         return None	