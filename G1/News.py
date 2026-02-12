import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from bs4 import BeautifulSoup

def g1Economy():
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    url = 'https://g1.globo.com/economia/'

    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    boxHighlights = soup.find_all("div", class_ = 'bstn-hl-wrapper')
    
    dfNewsMat = pd.DataFrame(
        columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
       , index = [0, 1, 2, 3, 4, 5]
    )
    
    for i, news in enumerate(boxHighlights):
        topico = news.find("div", class_ = '_evt').span.text
        subtopico = news.find("p", elementtiming="text-csr")
        link = news.a['href']

        dfNewsMat.loc[i, 'manchete'] = 'Economia'
        dfNewsMat.loc[i, 'topico'] = topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico
        dfNewsMat.loc[i, 'link'] = link
        dfNewsMat.loc[i, 'jornal'] = 'g1'

        if i == (len(boxHighlights) - 1):
            break
        i += 1

    boxNewsMat = soup.find_all("div", class_ = 'feed-post bstn-item-shape type-materia')

    for i, news in enumerate(boxNewsMat):
        manchete = news.find("p", elementtiming = 'text-csr').text
        link = news.find("h2").a['href']
        topico = news.find("p", elementtiming="text-csr").text
        subtopico = news.find("div", class_ = 'feed-post-body-resumo').p.text
        
        dfNewsMat.loc[i, 'manchete'] = 'Economia'
        dfNewsMat.loc[i, 'topico'] =   topico #topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico  
        dfNewsMat.loc[i, 'link'] = link
        dfNewsMat.loc[i, 'jornal'] = 'g1'

        if i == 5:
            break
        i += 1

    # for i, news in enumerate(boxNewsVid):
    #     new = news.find("h2").text
    #     link = news.find("h2").a['href']
    #     topico = news.find("span", class_ = 'feed-post-metadata-section').text
    #     subtopico = None # news.find("div", class_ = 'feed-post-body-resumo').p.text
    #     dfNewsVid.loc[i, 'manchete'] = new
    #     dfNewsVid.loc[i, 'topico'] = topico #'tech'
    #     dfNewsVid.loc[i, 'subtopico'] = subtopico #"Economia"
    #     dfNewsVid.loc[i, 'link'] = link
    #     dfNewsVid.loc[i, 'jornal'] = 'g1'

    #     if i == 5:
    #         break
    # boxNewsVid = soup.find_all("div", class_ = ['feed-post bstn-item-shape type-video']) 
    # dfNewsVid = pd.DataFrame(
    #     columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
    #    , index = [0, 1, 2, 3, 4, 5]
    # )
    
    # dfNews = pd.concat([dfNewsMat, dfNewsVid], ignore_index=True)
    # return dfNews
    return dfNewsMat

def g1Tech():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://g1.globo.com/tecnologia/'

    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    boxHighlights = soup.find_all("div", class_ = 'feed-post bstn-item-shape type-materia')
    
    dfNewsMat = pd.DataFrame(
        columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
       , index = [0, 1, 2, 3, 4, 5]
    )
    
    for i, news in enumerate(boxHighlights):
        # topico = news.find("p", elementtiming = 'text-csr').text
        # subtopico = news.find("p", elementtiming = 'text-csr').text
        # topico = news.find('div', class_='_evt').h2.a.p.text
        topico = news.find('div', class_='_evt').p.text
        subtopico = news.find('div', class_='feed-post-body-resumo').p.text
        link = news.a['href']

        dfNewsMat.loc[i, 'manchete'] = 'Tech'
        dfNewsMat.loc[i, 'topico'] = topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico
        dfNewsMat.loc[i, 'link'] = link
        dfNewsMat.loc[i, 'jornal'] = 'g1'

        if i == 5:
            break
        i += 1

    return dfNewsMat

def brazilNews(tema):
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    if tema == 'economia':
        tema = 'Economia'
        url = 'https://braziljournal.com/categoria/economia/'
    elif tema == 'tech':
        tema = 'Tech'
        url = 'https://braziljournal.com/categoria/tecnologia/'
    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    boxHighlights = soup.find_all("figcaption", class_ = 'boxarticle-infos')
    dfNewsMat = pd.DataFrame(
        columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
       , index = [0, 1, 2, 3, 4, 5]
    )
    for i, news in enumerate(boxHighlights):
        
        topico = news.find("p", class_ = 'boxarticle-infos-tag').text
        subtopico = news.find("h2", class_ = 'boxarticle-infos-title').text
        link = news.find("h2", class_ = 'boxarticle-infos-title').a['href']

        dfNewsMat.loc[i, 'manchete'] = tema
        dfNewsMat.loc[i, 'topico'] = topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico
        dfNewsMat.loc[i, 'link'] = link
        dfNewsMat.loc[i, 'jornal'] = 'brazil journal'

        if i == 5:
            break
        i += 1

    return dfNewsMat

def valueEco(tema):

    if tema == 'economia':
        tema = 'Economia'
        url = 'https://valor.globo.com/financas/'
    elif tema == 'tech':
        tema = 'Tech'
        url = 'https://valor.globo.com/empresas/'
    
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    boxHighlights = soup.find_all("div", class_='highlight')
    dfNewsMat = pd.DataFrame(
        columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
       , index = [0, 1, 2, 3, 4, 5]
    )

    for i, news in enumerate(boxHighlights):
        topico = news.find("h3").a.text
        subtopico = news.find('h2').a['title']
        link = news.find("h2").a['href']

        dfNewsMat.loc[i, 'manchete'] = tema
        dfNewsMat.loc[i, 'topico'] = topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico
        dfNewsMat.loc[i, 'link'] = link
        dfNewsMat.loc[i, 'jornal'] = 'valor economico'

        if i == 5:
            break
        i += 1

    return dfNewsMat

def fortune(tema):

    if tema == 'economia':
        url = 'https://fortune.com/section/finance/'
    elif tema == 'tech':
        url = 'https://fortune.com/section/tech/'
    elif tema == 'ai':
        url = 'https://fortune.com/tag/artificial-intelligence/'
    
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    boxHighlights = soup.find_all("li", class_ = 'flex flex-col layout-gap-y-default')
    dfNewsMat = pd.DataFrame(
        columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
       , index = [0, 1, 2, 3, 4, 5]
    )

    for i, news in enumerate(boxHighlights):
        if tema != 'ia':
            topico = news.find("div", class_ = 'flex flex-col gap-sm').a.text
            subtopico = news.find("div", class_ = 'saa25045-2 jikDob').span.text
            link = news.find("div", class_ = 'flex flex-col gap-sm').a['href']
        else:
            topico = news.find("div", class_ = 'flex flex-col gap-sm').a
            subtopico = news.find("div", class_ = 'flex flex-col gap-sm').span.text

            for m, manch in enumerate(topico):
                if m == 1:
                    manchete = manch.span.text
                    link = manch['href']

        dfNewsMat.loc[i, 'manchete'] = tema
        dfNewsMat.loc[i, 'topico'] = topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico
        dfNewsMat.loc[i, 'link'] = link
        dfNewsMat.loc[i, 'jornal'] = 'fortune'

        if i == 5:
            break
        i += 1

    return dfNewsMat

def wsj(tema):

    if tema == 'economia':
        url = 'https://wsj.com/finance/'
    elif tema == 'tech':
        url = 'https://wsj.com/tech/'
    elif tema == 'ai':
        url = 'https://wsj.com/tech/ai/'
    
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    if tema == 'tech':
        boxHighlights = soup.find_all("div", attrs={'data-testid': 'allesseh'})
        dfNewsMat = pd.DataFrame(
            columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
        , index = [0, 1, 2, 3, 4, 5]
        )

        for i, news in enumerate(boxHighlights):
            manchete = news.find("h3", class_ = 'csv-fsvegl').a.span.p.text
            subtopico = '-'
            link = news.find("h3", class_ = 'csv-fsvegl').a['href']
    
            dfNewsMat.loc[i, 'manchete'] = manchete
            dfNewsMat.loc[i, 'topico'] = tema
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = link
            dfNewsMat.loc[i, 'jornal'] = 'wsj'

            if i == 5:
                break
            i += 1
        return dfNewsMat
    
    elif tema == 'economia':
        boxHighlights = soup.find_all("div", class_ = 'css-1yp7ne6')
        dfNewsMat = pd.DataFrame(
            columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
        , index = [0, 1, 2, 3, 4, 5]
        )

        for i, news in enumerate(boxHighlights):
            manchete = news.find("h3", class_ = 'csv-fsvegl').a.span.p.text
            subtopico = '-'
            link = news.find("h3", class_ = 'csv-fsvegl').a['href']
    
            dfNewsMat.loc[i, 'manchete'] = manchete
            dfNewsMat.loc[i, 'topico'] = tema
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = link
            dfNewsMat.loc[i, 'jornal'] = 'wsj'

            if i == (len(boxHighlights)-1) or i == 5:
                break
            i += 1
        
        boxHighlights = soup.find_all("div", class_ = 'css-18y1fei')
        
        for i, news in enumerate(boxHighlights):
            manchete = news.find("h3", class_ = 'csv-fsvegl').a.span.p.text
            subtopico = '-'
            link = news.find("h3", class_ = 'csv-fsvegl').a['href']
    
            dfNewsMat.loc[i, 'manchete'] = manchete
            dfNewsMat.loc[i, 'topico'] = tema
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = link
            dfNewsMat.loc[i, 'jornal'] = 'wsj'

            i += 1
            if i == 6:
                break

        return dfNewsMat

    elif tema == 'ia':
        boxHighlights = soup.find_all("div", class_ = 'css-bdm6mo')
        dfNewsMat = pd.DataFrame(
            columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
        , index = [0, 1, 2, 3, 4, 5]
        )

        for i, news in enumerate(boxHighlights):
            manchete = news.find("h3", class_ = 'csv-fsvegl').a.span.p.text
            subtopico = '-'
            link = news.find("h3", class_ = 'csv-fsvegl').a['href']
    
            dfNewsMat.loc[i, 'manchete'] = manchete
            dfNewsMat.loc[i, 'topico'] = tema
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = link
            dfNewsMat.loc[i, 'jornal'] = 'wsj'

            if i == 5:
                break
        
        return dfNewsMat

def ft(tema):

    if tema == 'economia':
        tema = 'Economia'
        url = 'https://ft.com/markets/'
    elif tema == 'tech':
        tema = 'Tech'
        url = 'https://ft.com/technology/'
    elif tema == 'deep_dive':
        tema = 'AI'
        url = 'https://ft.com/deep-dive/'
    
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    news = driver.find_element("xpath", "/html")
    html_not = news.get_attribute('outerHTML')
    soup = BeautifulSoup(html_not, 'html.parser')
    driver.quit()

    dfNewsMat = pd.DataFrame(
        columns = ['manchete', 'topico', 'subtopico', 'link', 'jornal']
       , index = [0, 1, 2, 3, 4, 5]
    )

    if tema != 'AI':
        boxHighlights = soup.find("div", attrs={'class':'o-teaser-collection o-teaser-collection--stream'})
        # boxHighlights = soup.find_all("div", class_ = 'o-teaser__content')

        try:
            subtopico = boxHighlights.find("p", attrs = {'class':'o-teaser__standfirst'}).a.text
        except:
            subtopico = '-'
        
        topico = boxHighlights.find("div", attrs={'class':'o-teaser__heading'}).a.text
        link = boxHighlights.find("p", attrs={'class':'o-teaser__standfirst'}).a['href']

        i = 0

        dfNewsMat.loc[i, 'manchete'] = tema
        dfNewsMat.loc[i, 'topico'] = topico
        dfNewsMat.loc[i, 'subtopico'] = subtopico
        dfNewsMat.loc[i, 'link'] = 'https://www.ft.com' + link
        dfNewsMat.loc[i, 'jornal'] = 'ft'
        
        boxHighlights = (soup.find("div", attrs = {'data-trackable':'top-stories-column-one'})).find_all("div",  class_ = "o-teaser__content")

        for _, news in enumerate(boxHighlights):
            i += 1

            try:
                topico = news.find("div", attrs = {'class': "o-teaser__heading"}).a.text
            except:
                topico = '-'

            subtopico = news.find("p", attrs={'class':'o-teaser__standfirst'}).a.text
            link = news.find("p", attrs={'class':"o-teaser__standfirst"}).a['href']
    
            dfNewsMat.loc[i, 'manchete'] = tema
            dfNewsMat.loc[i, 'topico'] = topico
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = 'https://www.ft.com' + link
            dfNewsMat.loc[i, 'jornal'] = 'ft'

            if i == 5:
                break

        boxHighlights = (soup.find("div", attrs = {'data-trackable':"opinion-and-analysis"})).find_all("div", class_ = "o-teaser__content")

        for _, news in enumerate(boxHighlights):
            i += 1

            try:
                topico = news.find("div", attrs = {'class':'o-teaser__heading'}).a.text
            except:
                topico = '-'

            subtopico = news.find("p", attrs={'class':'o-teaser__standfirst'}).a.text
            link = news.find("p", attrs={'class':"o-teaser__standfirst"}).a['href']

            dfNewsMat.loc[i, 'manchete'] = tema
            dfNewsMat.loc[i, 'topico'] = topico
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = 'https://www.ft.com' + link
            dfNewsMat.loc[i, 'jornal'] = 'ft'

            if i == 5:
                break
        return dfNewsMat

    else:
        editorial = soup.find_all('div', attrs = {'class':'o-teaser-collection__list js-stream-list'})
        i = 0

        for _, news in enumerate(editorial):
        
            # if news.find("div", attrs={'class':'o-ads__outer'}) == None: # pulando linhas com anúncio

            topico = news.find("a", attrs = {'class':"o-teaser__heading"}).text
            subtopico = news.find("p", attrs={'class':'o-teaser__standfirst'}).a.text
            link = news.find("p", attrs={'class':"o-teaser__heading"}).a['href']

            dfNewsMat.loc[i, 'manchete'] = tema
            dfNewsMat.loc[i, 'topico'] = topico
            dfNewsMat.loc[i, 'subtopico'] = subtopico
            dfNewsMat.loc[i, 'link'] = 'https://www.ft.com' + link
            dfNewsMat.loc[i, 'jornal'] = 'ft'
            
            if i == 5:
                break
            i += 1

        return dfNewsMat

def webScrapingNews():
    #br
    bj_e = brazilNews('economia')
    bj_t = brazilNews('tech')
    g1_e = g1Economy()
    g1_t = g1Tech()
    value_e = valueEco('economia')
    value_t = valueEco('tech')

    #externo
    ft_e = ft('economia')
    ft_t = ft('tech')
    ft_ai = ft('deep_dive')
    wsj_e = wsj('economia')
    wsj_t = wsj('tech')
    f_e = fortune('economia')
    f_t = fortune('tech')
    f_ai = fortune('ai')

    dfNews = pd.concat([bj_e, bj_t, g1_e, g1_t, value_e, value_t, ft_e, ft_t, ft_ai, wsj_e, wsj_t, f_e, f_t, f_ai]
                       , ignore_index=True)

    os.makedirs('files/', exist_ok=True)
    dfNews.to_csv('files/dfNews.csv', index=False)

if __name__ == "__main__":
    webScrapingNews()