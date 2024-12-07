import SferumAPI
from aiogram import Bot, Dispatcher
import json
from message_parser import message_parser
from random import choice
import asyncio
from aiogram.filters import Command

# Инициализация
dp = Dispatcher()
bot_path = ""


async def main():
    tasks = [dp.start_polling(bot), auto_parse()]

    await asyncio.gather(*tasks)


@dp.message(Command("info"))
async def info(message):
    print("инфо")
    msg_count = 10
    if pars_is_start:
        command = message.text.split(maxsplit=1)
        try:
            if len(command) > 1:
                msg_count = int(command[1])
        except ValueError:
            pass

    else:
        await bot.send_message(message.chat.id, "бот не был запущен!")

    if msg_count > 20:
        msg_count = 20
    local_msg = msg_memory[-1: -msg_count: -1]
    local_msg.reverse()
    for i in local_msg:
        try:
            tgbot_msg = message_parser(i)
            for j in tgbot_msg:
                await bot.send_message(chats_id[0], j)
                await asyncio.sleep(2)
        except Exception as x:
            print(x)
            continue
    await bot.delete_message(chats_id[0], message.id)


@dp.message(Command("start"))
async def start(message):
    global pars_is_start
    try:
        chats_id.append(message.chat.id)
        with open(bot_path + "bot_memory.txt", "w") as f1:
            f1.write(str(chats_id[0]))
            f1.write("\n")
            f1.write(str(msg_memory[-1]['conversation_message_id']))

    except AttributeError:
        with open(bot_path + "bot_memory.txt", "w") as f1:
            f1.write(str(chats_id[0]))
            f1.write("\n")
            f1.write(str(msg_memory[-1]['conversation_message_id']))
    await bot.send_message(chats_id[0], choice(start_fraze))


async def auto_parse():
    global pars_is_start
    if not pars_is_start:
        pars_is_start = not pars_is_start
        try:
            msg_history = api.messages.get_history(chat_id_sf, count=200, offset=0)["response"]["items"]
            msg_history.reverse()
            for i in msg_history:
                if 'conversation_message_id' in i.keys():
                    if i['conversation_message_id'] > msg_memory[-1]['conversation_message_id']:
                        msg_memory.append(i)
            while True:
                print("try sferum")
                msg_history = api.messages.get_history(chat_id_sf, count=200, offset=0)["response"]["items"]
                print(msg_history[0])
                msg_history.reverse()
                for i in msg_history:

                    if 'conversation_message_id' in i.keys():
                        if i['conversation_message_id'] > msg_memory[-1]['conversation_message_id']:
                            print(msg_memory[-1]['conversation_message_id'])
                            print(i)
                            msg_memory.append(i)
                            with open(bot_path + "bot_memory.txt", "w") as f1:
                                f1.write(str(chats_id[0]))
                                f1.write("\n")
                                f1.write(str(msg_memory[-1]['conversation_message_id']))
                                f1.flush()
                            ms = message_parser(i)
                            for j in ms:
                                if "@all" in j:
                                    await bot.send_message(chats_id[0], j)
                                    print("@all trigger")
                                    await asyncio.sleep(2)
                            if i['from_id'] in targets:
                                for j in ms:
                                    await bot.send_message(chats_id[0], j)
                                    await asyncio.sleep(2)
                await asyncio.sleep(30)
        except Exception:
            exit(1)


if __name__ == "__main__":
    with open(bot_path + 'settings.json') as json_file:
        data = json.load(json_file)
        remixdsid = data["remixdsid"]
        bot_token = data["telegram_bot_token"]
        chat_id_sf = data["chat_id"]
        targets = data["targets"]
        start_msg = data["start_msg"]
        start_fraze = data["start_fraze"]
    api = SferumAPI.SferumAPI(remixdsid=remixdsid)
    bot = Bot(bot_token)
    chats_id = [0]
    pars_is_start = False
    with open(bot_path + "bot_memory.txt", "r") as f1:
        chats_id[0] = int(f1.readline().rstrip("\n"))
        k = f1.readline().rstrip("\n")
        if k != "":
            start_msg = int(k)
    msg_memory = [{'conversation_message_id': start_msg}]
    asyncio.run(main())
