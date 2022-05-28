from vk_api.longpoll import Event, VkEventType

import config
import django_settings
from constructor import models
from vk_bot import Bot, User


def save_user(user: User) -> models.VkUser:
    user = models.VkUser(
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name
    )
    user.save()
    return user


def save_to_me_event(event: Event, bot_user: models.VkUser, bot: Bot) -> models.VkEvent:
    event = models.VkEvent(
        message_id=event.message_id,
        from_user=save_user(bot.get_user(event.user_id)),
        to_user=bot_user,
        text=event.text
    )
    event.save()
    return event


def save_from_me_event(event: Event, bot_user: models.VkUser, bot: Bot) -> models.VkEvent:
    event = models.VkEvent(
        message_id=event.message_id,
        from_user=bot_user,
        to_user=save_user(bot.get_user(event.user_id)),
        text=event.text
    )
    event.save()
    return event


def save_event(event: Event, bot_user: models.VkUser, bot: Bot) -> models.VkEvent:
    if event.to_me:
        return save_to_me_event(event, bot_user, bot)
    else:
        return save_from_me_event(event, bot_user, bot)


def save_bot(bot: Bot) -> models.VkUser:
    user = models.VkUser(
        user_id=bot.group['id'],
        first_name=bot.group['name'],
        is_bot=True
    )
    user.save()
    return user


def main():
    bot = Bot(config.VK_TOKEN, config.VK_API_VERSION)
    bot_user = save_bot(bot)
    long_poll = bot.get_vk_long_poll()
    print(f"Прослушка запущена https://vk.com/{bot.group['screen_name']}")
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            save_event(event, bot_user, bot)


if __name__ == '__main__':
    main()