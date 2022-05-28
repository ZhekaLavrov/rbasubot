import datetime
import json

import telebot
from asgiref.sync import sync_to_async
from telethon import TelegramClient, events
from telethon.events import CallbackQuery
from telethon.tl.types import Message

import config
import django_settings
from constructor import models

api_id = config.TELEGRAM_APP_API_ID
api_hash = config.TELEGRAM_APP_API_HASH

client = TelegramClient('saving_dialogs', api_id, api_hash)

bot = telebot.TeleBot(config.TELEGRAM_TOKEN, parse_mode=None)
bot_info = bot.get_me()
print(f"https://t.me/{bot_info.username}")
bot_user = models.TelegramUser(
    user_id=bot_info.id,
    first_name=bot_info.first_name,
    last_name=bot_info.last_name,
    username=bot_info.username,
    is_bot=bot_info.is_bot
)
bot_user.save()


def make_user(event):
    models.TelegramUser(
        user_id=event.chat.id,
        first_name=event.chat.first_name,
        last_name=event.chat.last_name,
        username=event.chat.username,
        is_bot=event.chat.bot
    ).save()


def make_telegram_message(message: Message):
    if message.out:
        models.TelegramMessage(
            message_id=message.id,
            from_user=bot_user,
            chat_id=message.peer_id.user_id,
            date=message.date,
            text=message.message,
            json=message.to_json()
        ).save()
    else:
        models.TelegramMessage(
            message_id=message.id,
            from_user_id=message.peer_id.user_id,
            chat=bot_user,
            date=message.date,
            text=message.message,
            json=message.to_json()
        ).save()


def save_call_back_query_message(message_id, from_user_id, chat, date, text, json):
    models.TelegramMessage(
        message_id=message_id,
        from_user_id=from_user_id,
        chat=chat,
        date=date,
        text=text,
        json=json
    ).save()


def get_button_text(button_id):
    text = models.Button.objects.filter(id=button_id)[0].text
    return text


@client.on(events.NewMessage())
async def new_message(event):
    await sync_to_async(make_user)(event=event)
    await sync_to_async(make_telegram_message)(message=event.original_update.message)
    e = event
    print(event)


@client.on(events.CallbackQuery())
async def call_back_query(event: CallbackQuery.Event):
    await sync_to_async(make_user)(event=event)
    e = event
    print(event.id)
    text = await sync_to_async(get_button_text)(event.data)
    await sync_to_async(save_call_back_query_message)(
        event.id,
        event.chat_id,
        bot_user,
        datetime.datetime.now(),
        text,
        event.original_update.to_json()
    )
    print(text)
    print(event)


client.start(bot_token=config.TELEGRAM_TOKEN)
print("Прослушка запущена")
client.run_until_disconnected()