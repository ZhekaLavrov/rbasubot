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
user_bot = models.TelegramUser(
    user_id=bot_info.id,
    is_bot=bot_info.is_bot,
    first_name=bot_info.first_name,
    last_name=bot_info.last_name,
    username=bot_info.username
)
user_bot.save()


def save_message(from_message, to, message_json):
    msg = models.TelegramMessage(
        message_id=message_json.get("message_id", 0),
        from_user=from_message,
        chat=to,
        date=datetime.fromtimestamp(message_json.get("date"), tz=timezone.utc),
        text=message_json.get("text"),
        reply_markup=message_json.get("reply_markup"),
        photos=message_json.get("photo"),
        json=message_json
    )
    msg.save()


@bot.message_handler(func=lambda message: True)
def message_answer(message: telebot.types.Message):
    user = models.TelegramUser(
        user_id=message.chat.id,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name,
        username=message.chat.username,
    )
    user.save()
    message_json = message.json
    save_message(user, user_bot, message_json)
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
        message_json = reply.json
        save_message(user, user_bot, message_json)
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
            message_json = reply.json
            save_message(user, user_bot, message_json)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery):
    user = models.TelegramUser(
        user_id=call.message.chat.id,
        first_name=call.message.chat.first_name,
        last_name=call.message.chat.last_name,
        username=call.message.chat.username,
    )
    user.save()
    callback_data = call.data
    models.CallBack(
        id=call.id,
        calldata=callback_data,
        from_user=user,
        chat=user_bot,
        date=datetime.now(tz=timezone.utc),
        message=call.message.json
    ).save()
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
            message_json = reply.json
            save_message(user, user_bot, message_json)
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
                message_json = reply.json
                save_message(user, user_bot, message_json)


bot.infinity_polling()
