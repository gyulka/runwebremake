import json

import requests

from flask import Blueprint, request
import sqlite3
from config import db, tg_token
import requests

tg = Blueprint('tg_api', __name__)


def method(method_name, data):
    return requests.post(f'https://api.telegram.org/bot{tg_token}/{method_name}', json=data)


def send_msg(chat_id, text, keyboard=None):
    return method('sendMessage', data={'chat_id': chat_id, 'text': text, 'reply_markup': keyboard})


def db_connect():
    return sqlite3.connect(db)


@tg.route('/', methods=['POST'])
def tg_api_handler():
    data = json.loads(request.data.decode('utf-8'))
    print(data)

    con = db_connect()
    try:
        con.execute('select id from users where id=?', (data['message']['from']['id'])).fetchone()
    except Exception:
        con.execute('insert into user(id) values(?)', (data['message']['from']['id'],))
    if data['message']['text'][0] == '/':
        if data['message']['text'] == '/start':
            send_msg(data['message']['from']['id'], 'привет я пока что не готов')
        elif data['message']['text'] == '/off':
            res = requests.post('http://localhost:4000/api/setupdates', json={'target': 'all', 'update': 'off'})
            if res.json()['success']:
                send_msg(data['message']['from']['id'], 'успешно, дождитесь выключения')
            else:
                send_msg(data['message']['from']['id'], 'что-то пошло не так')

    return {'ok': True}
