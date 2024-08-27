from aiogram import types, Bot, executor
from aiogram import Dispatcher
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio

import sqlite3

bot = Bot(token="")
# Диспетчер
dp = Dispatcher(bot,storage=MemoryStorage())

db = 'DB.db'

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        connection_obj = sqlite3.connect(db, check_same_thread=False)
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute("INSERT INTO users (id) VALUES(?)", (message.chat.id,))
        connection_obj.commit()
        connection_obj.close()
    except:
        pass


@dp.message_handler(commands=['hMk8zJB'])
async def start(message: types.Message):
    try:
        connection_obj = sqlite3.connect(db, check_same_thread=False)
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute(f"DELETE FROM users WHERE id = '{message.chat.id}'")
        cursor_obj.execute("INSERT INTO admins (id) VALUES(?)", (message.chat.id,))
        connection_obj.commit()
        connection_obj.close()
        await message.answer('Добро пожаловать в админы')
    except:
        await message.answer('Вы уже админ')


@dp.message_handler(commands=['send'])
async def number(message: types.Message):
    try:
        connection_obj = sqlite3.connect(db, check_same_thread=False)
        cursor_obj = connection_obj.cursor()
        admin = cursor_obj.execute(f"SELECT EXISTS(SELECT id FROM admins WHERE id = '{message.chat.id}')").fetchall()[0][0]
        users = cursor_obj.execute(f"SELECT id FROM users").fetchall()
        connection_obj.close()
        if admin == 1:
            for user in users:
                try:
                    await bot.send_message(user[0],message.text.split(' ',1)[1])
                except BotBlocked:
                    pass
            await message.answer('Рассылка отправлена')
    except Exception as error:
        print(error)
        await message.answer('Что-то пошло не так')

@dp.message_handler()
async def number(message: types.Message):
    await message.delete()
    await message.answer('')#Запуск веб приложения

executor.start_polling(dp,skip_updates=True)