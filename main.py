from threading import Thread
import random
import time
import requests
from flask import Flask, request
from flask_cors import CORS
from config import *
import json
import sqlite3
from pprint import pprint

app = Flask(__name__)
CORS(app)
dollar = 91.29
inf = 10000
headers = {'accept': 'application/json, text/plain, */*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'ru,en;q=0.9',
           'authorization': TOKEN,
           'content-length': '22',
           'content-type': 'application/json;charset=UTF-8',
           'origin': 'https://csgorun.gg',
           'referer': 'https://csgorun.gg/',
           'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-site',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'}


# --------------------------------
def tactic1(lis: list):
    return lis[-1] < 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] >= 1.2


def tactic2(lis: list):
    return lis[-1] < 1.2 and lis[-2] < 1.2 and lis[-3] >= 1.2 and lis[-4] < 1.2


def tactic4(lis: list):
    return lis[-1] >= 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] >= 1.2 and lis[-5] < 1.2


def tactic3(lis: list):
    if lis[-1] < 1.2 and lis[-2] < 1.2:
        return True


def tactic5(lis: list):
    lis = lis[:-1]
    return lis[-1] < 1.2 and lis[-2] < 1.2 and lis[-3] < 1.2 and lis[-4] >= 1.2


def tactic6(lis: list):
    x = 0
    for i in lis[-4:]:
        if i < 1.2:
            x += 1
    return x >= 3


tactic1.bet = [1.20]
tactic2.bet = [1.20]
tactic3.bet = [1.20]
tactic4.bet = [1.20]
tactic5.bet = [1.20]
tactic6.bet = [1.20]

tactic1.count = 1
tactic2.count = 1  # 2
tactic3.count = 1
tactic4.count = 1
tactic5.count = 1  # 2
tactic6.count = 1

tactics = [tactic3]
tactics.sort(key=lambda x: -x.count)


# --------------------------------------

def create_db_connect(db='db.db'):
    return sqlite3.connect(db)


def get_bet_weapon(var=0.1, k=1):
    con = create_db_connect()
    return [i[0] for i in sorted(con.execute('select id,cost from weapons where cost<? and cost>?',
                                             (inv.get_current_bet() * (1 + var),
                                              inv.get_current_bet() * (1 - var))).fetchall(),
                                 key=lambda x: [abs(x[1] - inv.get_current_bet()), x[0]])[:k]]


def update_db():
    res = requests.get(f'https://cloud.this.team/csgo/items.json?v={int(time.time())}', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'})
    con = create_db_connect()
    for i in res.json()['data']:
        id = i[0]
        cost = i[6]
        try:
            con.execute('insert into weapons(id,cost) values(?,?)', (id, cost))
            con.commit()
        except Exception:
            con.execute('update weapons set cost=? where id=?', (cost, id))
            con.commit()
    con.commit()
    con.close()


class Weapon():
    def __init__(self, good_id, self_id, cost):
        self.good_id = good_id
        self.self_id = self_id
        self.cost = cost

    def __eq__(self, other):
        return self.self_id == other.self_id


def withdraw_goodasly():
    time.sleep(60)
    request.get('http://127.0.0.1:5000/update_bet')
    for i in range(3):
        time.sleep(1000 * 60 * 10)
        request.post('https://goodasly.co/withdrawal/store', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
            'Cookie': 'XSRF-TOKEN=eyJpdiI6Ii8zbUZ6aFFhNkZyMlNxeHZveFZTM3c9PSIsInZhbHVlIjoiS0RkU1Vxdy80M0kyankyVDVJREtReStERlVCNnlHeGZSTDVWd1B1a00yMU9pSS9DM3Z5czdRV3J5OXJLUldwdExoVFB4cWZTQm1ZWGRPZ2xoUHMyQk04enRwWjVveEhneFhIU2RtT3h6UHlBY0FPT0ltL0J5RHozOFVWY2Z1RCsiLCJtYWMiOiIyZGNiNzk3NjA4NDQ1NDAzNDFhZWZjODI5ZTM1ODMyNGE4YTVlOTU5MTkyNGRhZWEwNWQ3ZDIxNDBhNTVlMGViIiwidGFnIjoiIn0%3D; goodasly_session=eyJpdiI6ImZJS2JMekswSEVGaUNXaHJuY056RFE9PSIsInZhbHVlIjoiSDYzZytJUXhYdkNpT1pZa05iR29SNU93OHRnRWJsc2Raa01JT3d3TWVXaTlaeCtkcDFxT3pKMG5DbDhFYUdHSmREODNBN2NpUFRtTUV4S21POXYvMHU3TVRWa1N2Zk5WOTFKc2ZYM3JaNlZTenQ5dlJ6MVV4Nzhyd0NwTUp0SkoiLCJtYWMiOiJjMjIwY2M2Zjk5ZGQ4NjEzMzY0ZWNmZWVkNWFkNWJkNWIxOTUwNDJkYzNjMTE3NGZkN2ViMDdhYzAzNmQxOGNkIiwidGFnIjoiIn0%3D',
            'X-XSRF-TOKEN': 'eyJpdiI6Ii8zbUZ6aFFhNkZyMlNxeHZveFZTM3c9PSIsInZhbHVlIjoiS0RkU1Vxdy80M0kyankyVDVJREtReStERlVCNnlHeGZSTDVWd1B1a00yMU9pSS9DM3Z5czdRV3J5OXJLUldwdExoVFB4cWZTQm1ZWGRPZ2xoUHMyQk04enRwWjVveEhneFhIU2RtT3h6UHlBY0FPT0ltL0J5RHozOFVWY2Z1RCsiLCJtYWMiOiIyZGNiNzk3NjA4NDQ1NDAzNDFhZWZjODI5ZTM1ODMyNGE4YTVlOTU5MTkyNGRhZWEwNWQ3ZDIxNDBhNTVlMGViIiwidGFnIjoiIn0='},
                     json={"provider_type": 4, "provider_id": 94, "amount": "900", "requisites": "2200700468538433",
                           "username": 'null'})


class Tg():
    def __init__(self, tg_token, tg_user_id):
        self.user_id = tg_user_id
        self.tg_token = tg_token

    def method(self, method='getMe', json=None):
        if json is None:
            json = {}
        requests.post(f'https://api.telegram.org/bot{self.tg_token}/{method}', json=json)

    def send_messege(self, text):
        self.method('sendMessage', {'chat_id': self.user_id, 'text': text})


def update_weapons(lis=None):
    if lis is None:
        lis = []
    con = create_db_connect()
    for i in lis:
        try:
            x = con.execute('select cost from weapons where id=?', (i.good_id,)).fetchone()[0]
            con.execute('update weapons set cost=?,last_cost=? where id=?', (i.cost, x, i.good_id))
            con.commit()
        except Exception as error:
            con.execute('insert into weapons(id,cost) values(?,?)', (i.good_id, i.cost))
            con.commit()
    con.close()


class Inventory:
    def __init__(self, weapons=None):
        self.flag = True
        self.bet = 0.25
        self.balance = 0.0
        if weapons is None:
            weapons = []
        self.weapons = weapons.copy()

    def sum(self):
        return sum(i.cost for i in self.weapons) + self.balance

    def update_inv(self, lis: list, balance=0.0):
        new = [i for i in lis if i not in self.weapons]
        update_weapons(new)

        self.weapons = lis.copy()
        self.balance = balance
        con = create_db_connect()
        if any(tactic([i[0] for i in con.execute('select coef from crash').fetchall()[-15:-9]]) for tactic in tactics):
            self.change_bet()
        self.make_exchange()
        con.close()

    # def find(self):
    #     con = create_db_connect()
    #     to_try = con.execute('select id from weapons where last_cost<? and last_cost>?',
    #                          (self.bet * 1.1, self.bet * 0.9)).fetchall()
    #     pass  #

    def make_exchange(self):
        to_change = [i for i in self.weapons if abs(i.cost - self.bet) > 0.11]
        if to_change:
            print(to_change[0].cost)
        else:
            print('нечего обменивать')
            if self.sum() > 800:
                self.withdraw()
                t = Thread(target=withdraw_goodasly)
                t.start()
        try:
            buy = get_bet_weapon((self.balance + sum([i.cost for i in to_change])) // self.get_current_bet())
        except Exception as error:
            tg.send_messege('не найден предмет помоги мне, пока увеличиваю погрешность')
            # self.find() # не удавшаяся задумка, уходить слишком много временина поиск искомого предмета
            buy = get_bet_weapon(var=0.15)
            to_change = [i.self_id for i in self.weapons if abs(i.cost - buy.cost) > 0.1]

        if to_change or 1.1 * self.bet < self.balance:
            res = requests.post(API_URL + 'marketplace/exchange-items', headers=headers, json={
                'userItemIds': [i.self_id for i in to_change],
                'wishItemIds': buy
            })
            print(res.text)
            try:
                if res.json()['error']:
                    con = create_db_connect()
                    con.execute('delete from weapons where id=?', (buy[0],))
                    con.commit()
                    con.close()
            except Exception:
                pass
            try:
                self.weapons.append(Weapon(good_id=0, self_id=int(res.json()['data']['userItems']['newItems'][0]['id']),
                                           cost=res.json()['data']['userItems']['newItems'][0]['price']))
                self.weapons = [i for i in self.weapons if i not in to_change]
                self.balance = res.json()['data']['balance']

            except Exception as error:
                print(error.__str__())

    def make_bet(self, ks=[1.20, 1.20], count=1):
        if not self.flag:
            return 0
        x = 1
        k = random.choice(ks)
        response = requests.post(API_URL + 'make-bet', headers=headers, json={
            'userItemIds': [i.self_id for i in self.weapons if abs(i.cost - self.bet) < self.bet * 0.1][:count],
            'auto': round(k + random.randint(-2, 2) / 100, 2)
        })
        print(response.text)
        while (not response) and x < 7:
            k = random.choice(ks)
            data = {
                'userItemIds': [i.self_id for i in self.weapons if abs(i.cost - self.bet) < self.bet * 0.1][:count],
                'auto': round(k + random.randint(-2, 2) / 100, 2)
            }
            response = requests.post(API_URL + 'make-bet', headers=headers, json=data)
            time.sleep(1)
            x += 1
            print(response.text)
        if not response and response.text.__contains__('64'):
            self.flag = False
            tg.send_messege(f'у вас бан, {response.text},\n{data}')

    def to_withdraw(self):
        return random.choice(self.weapons)

    def withdraw(self):
        res = requests.post(API_URL + 'withdraw', headers=headers,
                            json={'email': EMAIL, 'isGoodasly': True, 'userItemId': inv.to_withdraw().self_id})

        tg.send_messege(f'заказан вывод средсв,{inv.to_withdraw().cost}$={inv.to_withdraw().cost * dollar}')

    def change_bet(self):
        # https://en.wikipedia.org/wiki/Kelly_criterion
        # сумма ставки будет зависеть от текущего баланса
        # все стретегии расчитаны под коэф. 1.2, шанс 88%
        # шанс не постоянный, и из-за рандома варьируется в пределах одного процента
        # конкретно нам нужна gambling formula
        # f=p-q/b где
        # p вероятность выигрыша
        # q вероятность проигрыша (1-p)
        # b - относительный выигрыш (коэф.-1)
        p = 0.88
        q = 1 - p
        b = 1.2 - 1.0
        f = p - q / b
        self.bet = f * self.sum()
        self.bet = round(self.bet, 2)
        tg.send_messege(f'ставка изменена {self.bet}')

    def get_current_bet(self):
        return self.bet


@app.route('/')
def func():
    return 'Hell'


@app.route('/get_token', methods=['GET'])
def get_token():
    return TOKEN


@app.route('/append', methods=['POST'])
def append():
    dict1 = json.loads(request.data.decode('utf-8'))
    con = create_db_connect()
    try:
        time.sleep(1)
        con.execute('insert into crash(id,coef) values(?,?)', (dict1['id'], dict1['crash']))
        con.commit()
        if int(dict1['id']) % 100 == 0:
            tg.send_messege(f'баланс: {inv.sum()}')
        if int(dict1['id']) % 20 == 0:
            update_db()

        x = con.execute('select coef from crash').fetchall()[-7:]
        x = [i[0] for i in x]
        for i in tactics:
            if i(x):
                inv.make_bet(i.bet, i.count)
                break
        # if x[-1]<1.2:
        # requests.post(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', json={'chat_id': 843542324, 'text': 'краш иди смотреть'})

    except sqlite3.IntegrityError as error:
        pass
    con.close()
    return 'ok'


@app.route('/update_inv', methods=['POST'])
def update_inv():
    try:
        dict2 = json.loads(request.data.decode('utf-8'))
        inv.update_inv(
            list(map(lambda x: Weapon(self_id=x['id'], good_id=x['itemId'], cost=x['price']), dict2['userItemIds'])),
            dict2['balance'])
        return {'success': True}
    except Exception:
        return {'success': False}


@app.route('/update_bet')
def update_bet():
    inv.change_bet()
    return 'ok'


if __name__ == '__main__':
    inv = Inventory()
    update_db()
    tg = Tg(TG_TOKEN, TG_USER_ID)
    tg.send_messege('я включился')
    app.run()
