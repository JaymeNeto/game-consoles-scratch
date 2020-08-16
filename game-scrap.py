import bs4
import re
import urllib.request as urllib_request
import pandas as pd
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def extrai_infos_console(nome_console):
    url2 = 'https://en.wikipedia.org/wiki/' + nome_console

    try:
        req = Request(url2)
        resp = urlopen(req)
    except URLError as e:
        print(e.reason)
    except HTTPError as e:
        print(e.status, e.reason)

    html = resp.read()
    html = html.decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')

    lista_infos = ['Console', 'Developer', 'Generation', 'Release date', 'Introductory price']

    dic_consoles = {}
    info_box = soup.find('table', class_='infobox hproduct vevent')
    dic_consoles['Console'] = [info_box.find('caption').getText()]
    infos = info_box.find('tbody').findAll('tr')

    for inf in infos:
        try:
            th = inf.find('th').getText()
        except:
            continue
        if th in lista_infos:
            dic_consoles[th] = [inf.find('td').getText()]
    return pd.DataFrame(dic_consoles)



url = 'https://en.wikipedia.org/wiki/Video_game_console'
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

tabela_consoles = soup.find('table', class_='wikitable').findAll('tr')

consoles = []
for linha in tabela_consoles:
    linha = linha.findAll('td')
    if len(linha) == 5:
        consoles.append(linha)


df = pd.DataFrame()
for console in consoles:
    nome = re.sub(' ', '_',console[0].getText('td'))
    try:
        df = df.append(extrai_infos_console(nome), ignore_index=True)
    except Exception as e:
        print('Erro na extração de: ' + nome + ' --- ')