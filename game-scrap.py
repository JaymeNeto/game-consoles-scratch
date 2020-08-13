import bs4
import re
import urllib.request as urllib_request
import pandas as pd

from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

url2 = 'https://en.wikipedia.org/wiki/Video_game_console'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

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

tabela_consoles = soup.find('table', class_='wikitable').findAll('tr')

consoles = []
for linha in tabela_consoles:
    linha = linha.findAll('td')
    if len(linha) == 5:
        consoles.append(linha)

dic_consoles = {'Console':[], 'Release year': [], 'Original price': [], 'Inflation 2020': [], 'Global Sales': []}
for console in consoles:
   dic_consoles['Console'].append(console[0].getText('td'))
   dic_consoles['Release year'].append(int(console[1].getText('td')))
   dic_consoles['Original price'].append(console[2].getText('td'))
   dic_consoles['Inflation 2020'].append(console[3].getText('td'))
   quant = re.sub(',','',console[4].getText('td'))
   quant = re.match('(\d+)', quant).group()
   dic_consoles['Global Sales'].append(int(quant))
df_consoles = pd.DataFrame(dic_consoles)

df_consoles.to_csv('consoles.csv', index=False)