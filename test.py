import requests
import http
from config import TOKEN

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'If-None-Match': "5c25-coA7Co7r+BC2KKLyUVnbiqkfH00",
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'authorization': TOKEN,
           'TE': 'trailers',
           'Connection': 'keep-alive',
           'content-type': 'application/json;charset=UTF-8',
           'origin': 'https://csgo5.run/',
           'referer': 'https://csgo5.run/',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'cross-site',
           'Host': 'smtpfast.com',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}
session= requests.session()

res = requests.get('https://smtpfast.com/current-state?montaznayaPena=null', headers=headers)
print(res)
f1=open('file.txt','wb')
print(res.)
f1.write(res.content)
