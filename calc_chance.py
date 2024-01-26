import sqlite3

con = sqlite3.connect('db.db')
lis = []
a, b = 0, 0

import requests
import time

# for i in range(4500727+1, 5497817):
#     res = requests.get(f'https://onemails.net/games/{i}')
#     value = res.json()['data']['crash']
#     con.execute('insert into crash(id,coef) values(?,?)', (i, value))
#     con.commit()
#     time.sleep(0.5)
k=1.2
for id, coef in sorted(con.execute('select id,coef from crash').fetchall()):
    lis.append(coef)
    if len(lis) == 7:
        lis = lis[1:]
        if lis[0] < 1.2 and lis[1] < 1.2 and lis[2]<1.2 and lis[3]>=1.2 and lis[4]<1.2:
            if lis[-1] >= k:
                a += 1
            else:
                b += 1

print(a / (a + b) * 100-1/k*100)
print(a+b)
