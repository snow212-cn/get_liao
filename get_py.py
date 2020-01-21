import requests
from bs4 import BeautifulSoup
import time
import os

site = 'https://www.liaoxuefeng.com'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

def save_soup(title, s, i = 0):
    for img in s.select('img'):
        img['src'] = site + img['data-src']
    for ifr in s.select('iframe'):
        ifr.extract()
    s.head.append(s.new_tag('meta', charset='utf-8'))
    title_tag = s.new_tag('title')
    title_tag.string = title
    s.head.append(title_tag)
    h1 = soup.new_tag('h1')
    h1.string = title
    s.body.insert(0, h1)
    with open('%s.%s.html' % (i, title), 'w') as f:
        f.write(str(s))

r = requests.get(site + '/wiki/1016959663602400', headers = headers)
soup = BeautifulSoup( r.content)
links = soup.body.select('#x-wiki-index>div')[0].find_all('a')
div = soup.body.select('#x-content>div.x-wiki-content.x-main-content')[0]
save_soup('Python教程', BeautifulSoup(div.prettify(),'html5lib'))

for i, a in enumerate(links):
    title = a.string.replace('/', '／')
    filename = '%s.%s.html' % (i, title)
    if os.path.exists(filename):
        print('file exists ' + filename)
        continue
    print('getting page:%s %s' % (title , a['href']))
    r = requests.get(site + a['href'], headers = headers)
    soup = BeautifulSoup(r.content)
    div = soup.body.select('#x-content>div.x-wiki-content.x-main-content')[0]
    save_soup(title, BeautifulSoup(div.prettify(),'html5lib'), i)
    time.sleep(1)
print('all finished')