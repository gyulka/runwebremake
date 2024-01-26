import config
import requests
from aiogram import Bot
from aiogram import types as tg_types
from aiogram import Dispatcher
from aiogram import filters, executor

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
import sqlite3
from config import tg_token, db

tgbot = Bot(tg_token)
dp = Dispatcher(tgbot)


def db_connect():
    return sqlite3.connect(db)


@dp.message_handler(commands=['start'])
async def message_handler(message: tg_types.Message):
    print(message.from_user.id)
    if message.from_user.id == config.TG_USER_ID:
        print(message.text)
        keyboard = InlineKeyboardMarkup()
        con = db_connect()
        x = con.execute('select id,ison,name from bots').fetchall()
        for id, ison, name in x[:5]:
            keyboard.add(InlineKeyboardButton(callback_data=f'bot_view_{id}', text=f'{name}{"🟢" if ison else "❌"}'))

        await message.answer('привет', reply_markup=keyboard)


@dp.message_handler(commands=['new'])
async def func1(message: tg_types.Message):
    if message.from_user.id == config.TG_USER_ID:
        await message.answer('привет')


if __name__ == '__main__':
    executor.start_polling(dp)
