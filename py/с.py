from time import sleep
from random import randint, choice
from requests import get, post
from bs4 import BeautifulSoup
from googletrans import Translator
from utilites import load, dump

import re

translator = Translator()

deps = '''правила экспертной системы
антиген коронавируса
антигены семейства коронавирусов
белки иммуноглобулина
возможность заражения
иммуноглобулин
датчик тока
держатель вала
забор биоматериала
антитела
микрокомпьютер
микроконтроллер
микрокомпьютер Raspberry Pi
микросхемы управления
коронавирус sars-cov-2
образец крови
образец сыворотки
пластик petg
плата Arduino Mega 2560
среда моделирования blender
понижающий преобразователь напряжения lm2596
сервопривод mg996r
экспресс анализатор
nasopharyngeal mucosa
nasopharyngeal velour swab'''.split('\n')

deps = '''РНК
ИФА
SARS-CoV-2
GB
SSH
HTTP
IDE'''.split('\n')

from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import unquote

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

try:
    db = load('db.json')
except FileNotFoundError:
    db = {}

class NoDescriptionFound(Exception):
    pass

def to_link(url):
    try:
        html = get(url, headers=headers).content
        dom = BeautifulSoup(html, features="lxml")
        host = urlparse(url).netloc
        date = datetime.today()
        date = "%s.%s.%s" % (date.day, date.month, date.year)
        title = dom.title.text
    except AttributeError:
        if '.pdf' in url or \
           '.ppt' in url or \
           '.doc' in url or \
           '.xls' in url:
            title = unquote(url.split('/')[-1].split('.')[0])
        else:
            title = '(nototle)'
    return f"[ {title} // {host} URL: {url} (дата обращения: {date}) ]"

def get_descr(term):
    useragents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Linux i686; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; Trident/4.0;)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPod; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (iPad; CPU OS 11_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_5_1 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/90.0",
        "Mozilla/5.0 (Android 11; Mobile; LG-M255; rv:90.0) Gecko/90.0 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPod touch; CPU iPhone 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 EdgiOS/46.3.13 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 Edge/40.15254.603",
        "Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 YaBrowser/21.6.3.883 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 YaBrowser/21.6.3.883 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (iPod touch; CPU iPhone 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 YaBrowser/21.6.3.883 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (Linux; arm_64; Android 11; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.3.4.59 Mobile Safari/537.36",
    ]
    def parse_dukcduckgo (term):
        sleep(randint(0,5))
        x = post(
    		'https://html.duckduckgo.com/html/', 
    		data={'q':term.replace(' ', '+')}, 
    		headers = {'user-agent': choice(useragents),},
            timeout=5
        ).content
        dom = BeautifulSoup(x, features="html5lib")
        open(f'/tmp/{term}.html','w').write(dom.prettify())
        try:
            text = dom.find('div', {'class':'zci'}).text
            link = to_link(dom.find('a', {'class':'result__a'})['href'])
        except AttributeError:
            try:
                text = dom.find('div', {'class':'result results_links results_links_deep web-result'}).text
                link = to_link(dom.find('a', {'class':'result__a'})['href'])
            except AttributeError:
                raise NoDescriptionFound
            
    
        return text, link
    
    try:
        text, link = parse_dukcduckgo(term)
        result = translator.translate(text, src='en', dest='ru').text
    except AttributeError:
        result = text
    except NoDescriptionFound:
        result, link = '', ''
        
    return re.sub(r'\s+', ' ', result.replace('\n',' ')), link 


for dep in deps:
    try:
        db[dep]
    except KeyError:
        descr = get_descr(dep)
        db.update({dep:descr})
        print(f' - {dep}: {descr}')
        dump(db, 'db.json')
    