import asyncio
from aiogram import Bot, Dispatcher
import logging

from handlers import start, posts_pika
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    # вариант регистрации роутеров по одному на строку
    dp.include_router(start.router)
    dp.include_router(posts_pika.router)


    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("Bot is starting...")
    asyncio.run(main())