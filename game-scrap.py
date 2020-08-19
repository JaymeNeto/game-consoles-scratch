import json, requests, re, bs4
import urllib.request as urllib_request
import pandas as pd
import numpy as np

from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def extrai_geracao_consoles(soup, geracao):

    consoles = [] 
    precos = [] 
    empresas = [] 
    vendas = [] 

    tabelas_consoles = soup.find('span', id=re.compile(r'Comparison')).parent.find_next_siblings('table')

    for tabela in tabelas_consoles:
        
        try:
            linha = tabela.find('th', text=re.compile(r'Manufacturer|Developer')).find_next_siblings()
            for empresa in linha:
                empresas.append(empresa.getText(strip=True))
        except:
            continue
        
        nomes = tabela.find('th', text=re.compile(r'(Name|Console)')).find_next_siblings()
        for nome in nomes:
            consoles.append(nome.getText(' - ',strip=True).split(' - ')[0])
        gen = len(consoles)*[geracao]

        linha = tabela.find('th', text=re.compile(r'Launch price')).find_next_siblings()
        for col in linha:
            precos.append(col.getText(strip=True))

        try:
            linha = tabela.find('th', text="Sales\n").find_next_siblings()
            for total in linha:
                vendas.append(total.getText(' - ', strip=True).split(' - ')[0])
            df_temp = pd.DataFrame(data=np.array([consoles, empresas, gen, precos, vendas]).T, columns=['Console', 'Empresa', 'Geração', 'Preco de lançamento', 'Vendas']).set_index('Console')
            
        except:
            df_temp = pd.DataFrame(data=np.array([consoles, empresas, gen, precos]).T, columns=['Console', 'Empresa', 'Geração', 'Preco de lançamento']).set_index('Console')
            df_temp = df_temp.join(extrai_Sales(soup))

    return df_temp

def extrai_Sales(soup):
    vendas = []
    tabela_vendas = soup.find('span', {'id': re.compile(r'(sales|Sales)')}).parent.find_next_siblings('table')[0]
    linhas = tabela_vendas.findAll('tr')
    colunas = linhas[0].getText(' - ', strip=True).split(' - ')[:2]
    for linha in linhas[1:]:
        vendas.append(linha.getText(' - ', strip=True).split(' - ')[:2])
    resultado = pd.DataFrame(data=np.array(vendas), columns=colunas).set_index('Console')
    resultado.columns = ['Vendas']
    return resultado

geracoes = ['First', 'Second', 'Third', 'Fourth']

consoles = pd.DataFrame()

for geracao in geracoes:
    url = 'https://en.wikipedia.org/wiki/%s_generation_of_video_game_consoles' % geracao
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    try:
        req = Request(url)
        resp = urlopen(req)
    except URLError as e:
        print(e.reason)
    except HTTPError as e:
        print(e.status, e.reason)


    html = resp.read()
    html = html.decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')

    consoles = consoles.append(extrai_geracao_consoles(soup, geracao))

consoles['Preco de lançamento'] = consoles['Preco de lançamento'].apply(lambda x : re.sub('( |\[).+','',x))

consoles.to_csv('consoles.csv')