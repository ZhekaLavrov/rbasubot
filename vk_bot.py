import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id

import config
import django_settings
from constructor import models


class User(object):
    def __init__(self, user_id: int, first_name: str, last_name: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name


class Bot(object):
    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version
        self.vk_session = vk_api.VkApi(token=self.token, api_version=self.api_version)
        self.vk = self.vk_session.get_api()
        self.group = self.get_group()
        self.set_group_settings()
        self.set_group_long_poll_settings()

    def get_group(self):
        group = self.vk.groups.getById()[0]
        return group

    def set_group_settings(self):
        return self.vk.groups.setSettings(
            group_id=self.group['id'],
            messages=1,
            bots_capabilities=1,
            bots_start_button=1
        )

    def set_group_long_poll_settings(self):
        self.vk.groups.setLongPollSettings(
            group_id=self.group['id'],
            enabled=1,
            api_version=self.api_version,
            message_new=1,
            message_reply=1,
            message_event=1
        )

    def get_vk_long_poll(self):
        return VkLongPoll(self.vk_session)

    def send_message(self, user_id, text, keyboard=None):
        try:
            return self.vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message=text,
                keyboard=keyboard
            )
        except:
            print(f"Не удалось отправить сообщение {user_id=}")

    def get_user(self, user_id: int) -> User:
        user = self.vk.users.get(user_ids=user_id)[0]
        user: dict
        return User(
            user_id=user.get("id"),
            first_name=user.get("first_name"),
            last_name=user.get("last_name")
        )


class Message(object):
    def __init__(self, text, next_message, keyboard=None):
        self.text = text
        self.next_message = next_message
        self.keyboard = keyboard


def create_message(trigger):
    if trigger is not None:
        next_message = trigger.next_message
        text = next_message.text
        next_message_buttons = models.Button.objects.filter(message=next_message).order_by("number")
        keyboard = None
        if len(next_message_buttons):
            keyboard = VkKeyboard(inline=True)
            for i, button in enumerate(next_message_buttons):
                if button.link:
                    keyboard.add_openlink_button(button.text, button.link, payload={"type": "my_type"})
                else:
                    keyboard.add_button(button.text, payload={"type": "my_type"})
                if i % 2 != 0 and len(next_message_buttons)-1 != i:
                    keyboard.add_line()
            keyboard = keyboard.get_keyboard()
        return Message(text, next_message, keyboard)


def get_trigger(text):
    trigger = None
    triggers = models.Trigger.objects.filter(button__text=text)[:1]
    if len(triggers):
        trigger = triggers[0]
    else:
        triggers = models.Trigger.objects.filter(text=text.lower())[:1]
        if len(triggers):
            trigger = triggers[0]
    return trigger


def get_next_message_trigger(message):
    trigger = None
    triggers = models.Trigger.objects.filter(message=message)[:1]
    if len(triggers):
        trigger = triggers[0]
    return trigger


def start_handler(event, bot: Bot):
    text = "Для общения с ботом используйте кнопки. Если хотите связаться с администрацией группы, просто напишите " \
           "свой вопрос "
    keyboard = VkKeyboard()
    keyboard.add_button("Начать")
    keyboard = keyboard.get_keyboard()
    try:
        payload = event.payload
    except AttributeError:
        payload = {}
    if payload == '{"command":"start"}':
        bot.send_message(
            event.peer_id,
            text,
            keyboard
        )


def handler(event, bot):
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            text = event.text
            message = create_message(get_trigger(text))
            if message is not None:
                bot.send_message(event.user_id, message.text, message.keyboard)
                trigger = get_next_message_trigger(message.next_message)
                if trigger is not None:
                    message = create_message(trigger)
                    bot.send_message(event.user_id, message.text, message.keyboard)


def main():
    bot = Bot(config.VK_TOKEN, config.VK_API_VERSION)
    long_poll = bot.get_vk_long_poll()
    print(f"Бот запущен - https://vk.com/{bot.group['screen_name']}")
    for event in long_poll.listen():
        start_handler(event, bot)
        handler(event, bot)


if __name__ == '__main__':
    main()
