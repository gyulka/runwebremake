import datetime
import sqlite3
import json
from flask import Flask, request
import tg
import api
from collections import defaultdict

app = Flask(__name__)
from config import db

updates = defaultdict(list)


@app.route("/<id>")
def index(id):
    con = sqlite3.connect(db)

    x = con.execute('select id,date,ison from users where id=?', (id,)).fetchone()
    print(x)
    dbdate = x[1]

    if x is not None and not x[-1] and datetime.datetime(year=int(dbdate.split('-')[0]),
                                                         month=int(dbdate.split('-')[1]),
                                                         day=int(dbdate.split('-')[2].split()[
                                                                     0])) > datetime.datetime.now():
        con.execute('update users set ison=1 where id=?', (id,))
        con.commit()
        ans = f'{id}'
    else:
        ans = '0'
    con.close()
    return ans


@app.route('/off/<id>')
def off(id):
    con = sqlite3.connect(db)

    con.execute('update users set ison=0 where id=?', (id,))
    con.commit()
    ans = f'ok'
    con.close()
    return ans


@app.route('/rm/<id>')
def rm(id):
    ans = 'ok'
    con = sqlite3.connect(db)
    con.execute('delete from users where id=?', (id,))
    con.commit()
    con.close()
    return ans


@app.route('/add')
def add():
    ans = 'ok'
    con = sqlite3.connect(db)
    dict2 = json.loads(request.data.decode('utf-8'))
    id, date = dict2['id'], dict2['date']
    if date == 1:
        date = datetime.timedelta(weeks=1)
    else:
        date = datetime.timedelta(days=30)
    try:
        con.execute('insert into users(id,date) values(?,?)', (id, datetime.datetime.now() + date))
    except Exception:
        id, dbdate = con.execute('select id,date from users where id=?', (id,)).fetchone()
        x = datetime.datetime(year=int(dbdate.split('-')[0]), month=int(dbdate.split('-')[1]),
                              day=int(dbdate.split('-')[2].split()[0]))
        x = max(x, datetime.datetime.now())
        con.execute('update users set date=? where id =?',
                    (date + x, id))
    con.commit()
    con.close()
    return ans


app.register_blueprint(tg.tg, url_prefix='/tg')
app.register_blueprint(api.api, url_prefix='/api')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
