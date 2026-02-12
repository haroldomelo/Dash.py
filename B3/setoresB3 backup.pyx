import pandas as pd
from pyparsing import col
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
import zipfile
import os
from pathlib import Path
from openpyxl import load_workbook

def setorB3():

    options = Options()
    options.headless = False
    diretorio = Path(__file__).parent

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "bvmf_iframe")))

    lclBtn1 = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[1]/div/div/a/i'
    lclBtnFind1 = driver.find_element('xpath', lclBtn1)
    # lclBtnFind1.click() # não deu certo
    driver.execute_script("arguments[0].click();", lclBtnFind1)

    # bdLink = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/div[2]/div[3]/div[2]/p/a' 
    # bd = driver.find_element('xpath', bdLink)
    # # bd.click() # não deu certo
    # driver.execute_script("arguments[0].click();", bd)

    # Adicionar espera para o elemento bdLink aparecer após o clique
    bdLink = '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/div[2]/div[3]/div[2]/p/button'
    try:
        bd = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, bdLink))
        )
        driver.execute_script("arguments[0].click();", bd)
    except Exception as e:
        print(f"Erro ao encontrar ou clicar no link de download: {e}")
        driver.quit()
        return None
    
    # ncessário utilizar para dar tempo necessário para o download do arquivo.
    time.sleep(5) 

    driver.quit()

    # Drive da pasta download
    # o "r" se faz necessário porque as \ (barras) do windows são invertidas. Assim, ele funciona como uma exceção no uso do SO Windows. Os demais SO, não se faz necessário 
    pathDownload = r"C:\Users\Haroldo Melo\Downloads"
    # pathDownload = Path(__file__).parent
    # pathDownload = str(pathDownload).replace("/", "\\") # substitui as / (barras) do linux pelas \ (barras) do windows

    # arqZip = zipfile.ZipFile(pathDownload + r"\ClassifSetorial.zip")
    xlsx_path = pathDownload + r"\ClassifSetorial.xlsx"
    headerDF = []
    ind = []

    # for bd in arqZip.namelist():
    # wb = load_workbook(filename=arqZip.open(bd), read_only=False)
    wb = load_workbook(filename=xlsx_path, read_only=False)
    ws = wb.active
    # setores = pd.read_excel(arqZip.open(bd), header=None)
    setores = pd.read_excel(xlsx_path, header=None)

    mgStart = None
    mgEnd = None  # Linha final da célula mesclada
    for merged_range in ws.merged_cells.ranges:
        rowS = merged_range.min_row - 1  # índice zero-based
        rowE = merged_range.max_row - 1    # índice zero-based

        if mgStart is None or rowS < mgStart:
            mgStart = rowS
            mgEnd = rowE
        elif rowS == mgStart:
            # Caso tenha mais de uma mesclagem iniciando na mesma linha, pega a maior final
            if rowE > mgEnd:
                mgEnd = rowE

    if mgStart is None:
        # Sem mesclagem, pega primeira linha não vazia
        h1 = setores.dropna(how='all').index[0]
        mgStart = h1
        mgEnd = h1

    # Header até a última linha da mesclagem (inclusive)
    header_df = setores.iloc[:mgEnd + 1, :]
    # print(f"Teste Header:\n{header_df}")

    header_df = header_df.ffill(axis=0) # vertical | se fosse axis=1 seria horizontal
    # print(f"Header após preenchimento:\n{header_df}")
    header = []
    for col in header_df.columns:
        vals = header_df[col].dropna().astype(str).values
        if len(vals) > 1:
            merged_header = ' - '.join(vals)
        elif len(vals) == 1:
            merged_header = vals[0]
        else:
            merged_header = ''
        header.append(merged_header)
    
    # Função para remover texto antes de " - "
    header2 = []
    for col in header:
        if " - " in col:
            header2.append(col.split(" - ", 1)[1])
        else:
            header2.append(col)

    print(f"Cabeçalho mesclado:\n{header2}")

    # Ler dados a partir da linha seguinte ao final da mesclagem
    data_row0 = mgEnd + 1

    df = pd.read_excel(xlsx_path, header=data_row0)

    # df.columns = header
    df.columns = header2
    # print(f'Dados a partir da linha {data_row0 + 1} (1-based):')
    # print(df.head())

    ind = []
    headerDF = []
    for index, col in enumerate(header2):
        if not str(col).startswith('Unnamed'):
            ind.append(index)
            headerDF.append(col)

    print('Colunas filtradas:')
    df = df.dropna(how='all', axis=0) # opera nas linhas
    df = df.dropna(how='all', axis=1) # opera nas colunas
    # print(headerDF)
    # print(setores)
    print(df)
        
    # setores['SUBSETOR'] = setores['SUBSETOR'].ffill()
        # setores['SETOR ECONÔMICO'] = setores['SETOR ECONÔMICO'].ffill()
    # setores = setores.dropna(subset = ['SEGMENTO'])
        # setores = setores.dropna(subset = ['LISTAGEM'])
        # setores = setores[['SETOR ECONÔMICO', 'SUBSETOR', 'SEGMENTO', 'LISTAGEM']]
    # setores = setores[['SUBSETOR', 'SEGMENTO', 'LISTAGEM']]

    # remove linhas que são iguais ao cabeçalho
    # setores = setores[~setores.eq(setores.columns).all(axis=1)]
    print(f"aqui: {df[df.columns]}")
    # df = df[~df.eq(df.columns).all(axis=1)]
    df = df[~df.eq(df.columns).all(axis=0)]
    # setores = setores.dropna() # remove linhas que tem valores n/a (null)
# df = df.dropna() # remove linhas que tem valores n/a (null)

    # df['SUBSETOR'] = df['SUBSETOR'].ffill()
    # df = df.dropna(subset = ['SEGMENTO'])
    # df = df[['SUBSETOR', 'SEGMENTO', 'LISTAGEM']]

    # # setores.columns # apresente o nome das colunas
    # df.columns # apresente o nome das colunas
    # # setores.columns = ['SUBSETOR', 'EMPRESA', 'TICKER'] # alterne o nome das colunas
    # df.columns = ['SUBSETOR', 'EMPRESA', 'TICKER'] # alterne o nome das colunas

    # # Removendo linhas duplicadas
    # # setores = setores.drop_duplicates()
    # df = df.drop_duplicates()
    
    # arqZip.close()
    print(pathDownload + r"\ClassifSetorial.xlsx")
    os.remove(pathDownload + r"\ClassifSetorial.xlsx") # agora deu certo
    # print(setores)
    # print(diretorio)
    print(df)
    print(diretorio)

    # Exportar dados tratados
    os.makedirs('B3', exist_ok=True)  # Cria o diretório se não existir
    df.to_csv("B3/setores.csv", index = False)
    df.to_parquet('B3/setores.parquet', index=False)