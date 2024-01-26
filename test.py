import requests
import config

import tg
# res= requests.get('http://runweb.temp.swtest.ru/add',json={'id':10,'date':1})
# print(res.text)
# # print(res.text)
# # config.myapi='http://localhost:4000/api/'
# res = requests.get(config.myapi+'setupdates',json={'update':'off','target':'all'})
# print(res.json())
res=requests.post(config.myapi+'bot_off',json={'id':1})
# res=requests.get(config.myapi+'get_updates',json={'target':1})
print(res.json())