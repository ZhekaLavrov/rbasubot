from datetime import datetime

import django_settings
from django.utils import timezone
import config
import telebot
from constructor import models

bot = telebot.TeleBot(config.TELEGRAM_TOKEN, parse_mode=None)
bot.set_my_commands(
    [telebot.types.BotCommand("start", "Начать")]
)
bot_info = bot.get_me()
print(f"https://t.me/{bot_info.username}")


@bot.message_handler(func=lambda message: True)
def message_answer(message: telebot.types.Message):
    triggers = models.Trigger.objects.filter(text=message.text.lower())[:1]
    if len(triggers):
        trigger = triggers[0]
        next_message = trigger.next_message
        text = next_message.text
        next_message_buttons = models.Button.objects.filter(message=next_message).order_by("number")
        buttons = telebot.types.InlineKeyboardMarkup()
        for button in next_message_buttons:
            buttons.row(telebot.types.InlineKeyboardButton(
                text=button.text,
                url=button.link,
                callback_data=str(button.id)
            ))
        reply = bot.send_message(message.chat.id, text, reply_markup=buttons)
        triggers = models.Trigger.objects.filter(message=next_message)[:1]
        if len(triggers):
            trigger = triggers[0]
            next_message = trigger.next_message
            text = next_message.text
            next_message_buttons = models.Button.objects.filter(message=next_message).order_by("number")
            buttons = telebot.types.InlineKeyboardMarkup()
            for button in next_message_buttons:
                buttons.row(telebot.types.InlineKeyboardButton(
                    text=button.text,
                    url=button.link,
                    callback_data=str(button.id)
                ))
            reply = bot.send_message(message.chat.id, text, reply_markup=buttons)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery):
    callback_data = call.data
    # print(call.message.json)
    button = models.Button.objects.filter(id=callback_data)[:1]
    if len(button):
        button = button[0]
        trigger = models.Trigger.objects.filter(button=button)[:1]
        if len(trigger):
            trigger = trigger[0]
            next_message = trigger.next_message
            text = next_message.text
            next_message_buttons = models.Button.objects.filter(message=next_message).order_by("number")
            buttons = telebot.types.InlineKeyboardMarkup()
            for button in next_message_buttons:
                buttons.row(telebot.types.InlineKeyboardButton(
                    text=button.text,
                    url=button.link,
                    callback_data=button.id
                ))
            reply = bot.send_message(call.message.chat.id, text, reply_markup=buttons)
            trigger = models.Trigger.objects.filter(message=next_message)[:1]
            if len(trigger):
                trigger = trigger[0]
                next_message = trigger.next_message
                text = next_message.text
                next_message_buttons = models.Button.objects.filter(message=next_message).order_by("number")
                buttons = telebot.types.InlineKeyboardMarkup()
                for button in next_message_buttons:
                    buttons.row(telebot.types.InlineKeyboardButton(
                        text=button.text,
                        url=button.link,
                        callback_data=button.id
                    ))
                reply = bot.send_message(call.message.chat.id, text, reply_markup=buttons)


bot.infinity_polling()
