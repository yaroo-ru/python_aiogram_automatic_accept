import contextlib
import asyncio
from aiogram.types import ChatJoinRequest
from aiogram import Bot, Dispatcher, F
import logging
import sqlite3


BOT_TOKEN = '00000:0000000'
CHANNEL_ID = -10000000
ADMIN_ID = 000000


async def approve_request(chat_join: ChatJoinRequest, bot: Bot):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Создаем таблицу Users
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER, username TEXT NOT NULL)")
    

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    # Вставляем значения в базу данных, после чего сохраняем и закрываем
    cursor.execute('INSERT OR IGNORE INTO Users (id, username) VALUES (?, ?)', (chat_join.from_user.id, chat_join.from_user.username))
    connection.commit()
    connection.close()
    
    message = f'<b>🔥 Рад приветствовать тебя в самом лучшем канале на свете.</b>\r\n\r\n' \
          f'Спасибо за подписку.\r\n\r\n'
    await bot.send_message(chat_id=chat_join.from_user.id, text=message)
    # Сообщение для админа или для тебя
    await bot.send_message(chat_id=000000, text=f'{chat_join.from_user.id}, {chat_join.from_user.username}')
    await chat_join.approve()


async def start():
    
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.chat_join_request.register(approve_request, F.chat.id ==CHANNEL_ID)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f'[Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())