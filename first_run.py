from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import Command

# Инициализация

bot_path = ""


async def main():
    dp = Dispatcher()
    bot = Bot(bot_token)
    tasks=[dp.start_polling(bot),auto_parse()]
    await asyncio.gather(*tasks)

@dp.message(Command("start"))
async def start(message):
    with open(bot_path + "bot_memory.txt", "w") as f1:
        f1.write(str(message.chat.id))
        f1.write("\n")
        f1.write(str(msg_memory[-1]['conversation_message_id']))


