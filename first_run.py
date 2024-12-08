from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import Command
from random import choice
import json

# Инициализация

bot_path = ""
dp = Dispatcher()

async def main():

    bot = Bot(bot_token)
    tasks=[dp.start_polling(bot)]
    await asyncio.gather(*tasks)

@dp.message(Command("start"))
async def start(message):
    with open(bot_path + "bot_memory.txt", "w") as f1:
        f1.write(str(message.chat.id))
        f1.write("\n")
    await bot.send_message(chats_id[0], choice(start_fraze))


if __name__ == "__main__":
    with open(bot_path + 'settings.json') as json_file:
        data = json.load(json_file)
        remixdsid = data["remixdsid"]
        bot_token = data["telegram_bot_token"]
        chat_id_sf = data["chat_id"]
        targets = data["targets"]
        start_msg = data["start_msg"]
        start_fraze = data["start_fraze"]
    asyncio.run(main())


