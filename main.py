import SferumAPI
import telebot
import time
import json
from random import randint

# Инициализация

with open('settings.json') as json_file:
    data = json.load(json_file)
    remixdsid = data["remixdsid"]
    bot_token = data["telegram_bot_token"]
    chat_id_sf = int(data["chat_id"])
    targets = data["targets"]

api = SferumAPI.SferumAPI(remixdsid=remixdsid)

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["ten_message"])
def ten_message(message):
    chat_id = message.chat.id
    try:
        messages_history = api.messages.get_history(peer_id=chat_id_sf, count=10, offset=0)
        ms = messages_history["response"]["items"][:]
        ms.reverse()
    except Exception:
        return
    for i in ms:
        try:
            if messages_history["response"]["items"][0]['attachments'] != [] and \
                    "photo" in messages_history["response"]["items"][0]['attachments'][0].keys():
                bot.send_message(chat_id,
                                 i['attachments'][0]["photo"]['orig_photo']['url'])
                bot.send_message(chat_id, i['text'] + '.')
                last_masage = i['conversation_message_id']
                continue
            if i["text"]:
                bot.send_message(chat_id, i["text"])
                # пересланные
            if 'fwd_messages' in i.keys():
                for i in i["fwd_messages"]:
                    print(chat_id, i)

                    if i['attachments'] != [] and \
                            "photo" in i['attachments'][0].keys():
                        bot.send_message(chat_id,
                                         i['attachments'][0]["photo"]['orig_photo']['url'])
                        bot.send_message(chat_id, i['text'] + '.')
                        print("yes")
                        continue
                    if messages_history["response"]["items"][0]["text"]:
                        bot.send_message(chat_id, i["text"])

            time.sleep(randint(1, 3) + randint(0, 10) / 10)
        except Exception as x:
            print(x)
            continue


@bot.message_handler(commands=["start"])
def start(message):
    global api
    chat_id = message.chat.id
    bot.send_message(chat_id, "бот запущен")
    messages_history = api.messages.get_history(peer_id=chat_id_sf, count=1, offset=0)  # peer_id - id чата в Сферум
    last_masage = messages_history["response"]["items"][0]['conversation_message_id']
    while True:
        try:
            messages_history = api.messages.get_history(peer_id=chat_id_sf, count=100, offset=0)
            # peer_id - id чата в Сферум
            if messages_history["response"]["items"][0]['conversation_message_id'] > last_masage and (
                    messages_history["response"]["items"][0]['from_id'] in targets or targets == []):
                print(chat_id, messages_history["response"]["items"][0])

                if messages_history["response"]["items"][0]['attachments'] != [] and \
                        "photo" in messages_history["response"]["items"][0]['attachments'][0].keys():
                    bot.send_message(chat_id,
                                     messages_history["response"]["items"][0]['attachments'][0]["photo"]['orig_photo'][
                                         'url'])
                    bot.send_message(chat_id, messages_history["response"]["items"][0]['text'] + '.')
                    last_masage = messages_history["response"]["items"][0]['conversation_message_id']
                    continue
                if messages_history["response"]["items"][0]["text"]:
                    bot.send_message(chat_id, messages_history["response"]["items"][0]["text"])

                    # пересланные
                if 'fwd_messages' in messages_history["response"]["items"][0].keys():
                    for i in messages_history["response"]["items"][0]["fwd_messages"]:
                        print(chat_id, messages_history["response"]["items"][0])

                        if i['attachments'] != [] and \
                                "photo" in i['attachments'][0].keys():
                            bot.send_message(chat_id,
                                             i['attachments'][0]["photo"]['orig_photo']['url'])
                            bot.send_message(chat_id, i['text'] + '.')
                            print("yes")
                            last_masage = messages_history["response"]["items"][0]['conversation_message_id']
                            continue
                        if messages_history["response"]["items"][0]["text"]:
                            bot.send_message(chat_id, i["text"])

                last_masage = messages_history["response"]["items"][0]['conversation_message_id']
            time.sleep(randint(1, 3) + randint(0, 10) / 10)
        except Exception as x:
            print(x)
            try:
                last_masage = messages_history["response"]["items"][0]['conversation_message_id']
            except KeyError:
                api = SferumAPI.SferumAPI(remixdsid=remixdsid)
                pass
            time.sleep(randint(1, 3) + randint(0, 10) / 10)


bot.polling(none_stop=True)
