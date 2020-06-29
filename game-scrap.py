import bs4
import urllib.request as urllib_request
import pandas

from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup


url2 = 'https://www.vgdb.com.br/consoles/'
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

titles = []
links = []
for li in soup.findAll('li'):
    try:
        games_name.append(li.a['title'])
        games_link.append(li.a['href'])
    except KeyError:
        pass

for t in titles:
    t = re.sun(' ','+', t)
    t = t + ' Console'
    wiki_search = 'https://en.wikipedia.org/w/index.php?cirrusUserTesting=glent_m0&search=' + t + '&title=Special%3ASearch&go=Go&wprov=acrw1_2'

    try:
        req = Request(wiki_search)
        resp = urlopen(req)
    except URLError as e:
        print(e.reason)
    except HTTPError as e:
        print(e.status, e.reason)

    html = resp.read()
    html = html.decode('utf-8')

    game_page = BeautifulSoup(html, 'html.parser')