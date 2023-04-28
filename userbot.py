from pyrogram import Client
from pyrogram.handlers import MessageHandler
import json
from pyrogram.enums import ParseMode
from pyrogram.types.messages_and_media.message import Message

with open('texts.json', 'r', encoding='utf8') as f:
    data = json.load(f)


api_id = data["api_id"]
api_hash = data["api_hash"]

app = Client("my_account", api_id=api_id, api_hash=api_hash)


async def my_function(client, message: Message):
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    for i in data['delete']:
        if i in message.text:
            break
    else:
        for i in data["message"]:
            if i in message.text:
                text = f'Отправитель - @{message.from_user.username}\nИз группы - @{message.chat.username}</a>\nЕго сообщение:\n\n<a href="{message.link}">{message.text}</a>'
                await app.send_message('me', text=text)
                await app.send_message(-959830717, text=text)
                break


my_handler = MessageHandler(my_function)
app.add_handler(my_handler)


app.run()
