from django.db import models


class Message(models.Model):
    text = models.TextField(
        help_text="Текст сообщения",
        null=True,
        verbose_name="Текст сообщения"
    )

    def __str__(self):
        count_symbols = 32
        if len(f"{self.text}") > count_symbols:
            return f"{self.text[:count_symbols]}..."
        else:
            return f"{self.text}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["id"]


class Button(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        help_text="Сообщение, к которому принадлежит кнопка"
    )
    text = models.CharField(
        max_length=40,
        help_text="Текст кнопки"
    )
    link = models.CharField(
        max_length=2048,
        help_text="Ссылка",
        null=True,
        default=None,
        blank=True
    )
    number = models.IntegerField(
        help_text="Порядковы номер кнопки в сообщении (от 1 до 10)",
        blank=True,
        null=True
    )

    def get_number(self):
        buttons = Button.objects.filter(message=self.message).order_by("number")
        if len(buttons):
            number = list(buttons)[-1].number
            number += 1
        else:
            number = 1
        return number

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = self.get_number()
        super(Button, self).save(*args, **kwargs)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"
        ordering = ["message", "id"]


class Trigger(models.Model):
    text = models.CharField(
        max_length=256,
        null=True,
        default=None,
        blank=True
    )
    button = models.ForeignKey(
        Button,
        on_delete=models.CASCADE,
        help_text="Кнопка, являющаяся триггером",
        null=True,
        default=None,
        blank=True
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        null=True,
        help_text="Сообщение, являющаяся триггером",
        default=None,
        blank=True
    )
    next_message = models.ForeignKey(
        Message,
        related_name="nextMessage",
        on_delete=models.CASCADE,
        null=True,
        help_text="Сообщение, которое будет отправлено при срабатывание триггера",
        default=None,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.text is not None:
            self.text = self.text.lower()
        super(Trigger, self).save(*args, **kwargs)

    def __str__(self):
        if self.text:
            text = f"Текст: {self.text}"
        elif self.button:
            text = f"Кнопка: {self.button.__str__()}"
        elif self.message:
            text = f"Сообщение: {self.message.__str__()}"
        else:
            text = f"{None}"
        text += f" -> {self.next_message.__str__()}"
        return text

    class Meta:
        verbose_name = "Триггер"
        verbose_name_plural = "Триггеры"
        ordering = ['id']


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(
        verbose_name="id",
        primary_key=True,
        help_text="id пользователя"
    )
    is_bot = models.BooleanField(
        help_text="Бот?",
        default=False
    )
    first_name = models.CharField(
        max_length=64,
        help_text="Имя пользователя telegram",
        null=True,
        default=None,
        blank=True
    )
    last_name = models.CharField(
        max_length=64,
        help_text="Фамилия пользователя telegram",
        null=True,
        default=None,
        blank=True
    )
    username = models.CharField(
        max_length=32,
        help_text="Имя пользователя (с @) telegram",
        null=True,
        default=None,
        blank=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["user_id"]

    def __str__(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.first_name}"


class TelegramMessage(models.Model):
    message_id = models.BigIntegerField(primary_key=True)
    from_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="from_user"
    )
    chat = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="chat"
    )
    date = models.DateTimeField(
        default=None,
    )
    text = models.TextField(
        null=True,
        default=None,
        blank=True
    )
    reply_markup = models.JSONField(
        null=True,
        default=None,
        blank=True
    )
    photos = models.JSONField(
        null=True,
        default=None,
        blank=True
    )
    json = models.JSONField(
        null=True,
        default=None,
        blank=True
    )

    class Meta:
        verbose_name = "Telegram сообщение"
        verbose_name_plural = "Telegram сообщения"
        ordering = ["date"]


class CallBack(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    calldata = models.CharField(max_length=64)
    from_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="call_from"
    )
    chat = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="call_to"
    )
    date = models.DateTimeField(
        default=None,
    )
    message = models.JSONField(
        null=True,
        default=None,
        blank=True
    )

    class Meta:
        verbose_name = "Telegram событие"
        verbose_name_plural = "Telegram события"
        ordering = ["date"]


class VkUser(models.Model):
    user_id = models.BigIntegerField(
        verbose_name="id пользователя ВКонтакте",
        primary_key=True,
        help_text="id пользователя ВКонтакте"
    )
    first_name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=255,
        help_text="Имя пользователя"
    )
    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        max_length=255,
        help_text="Фамилия пользователя",
        null=True,
        default=None,
        blank=True
    )
    is_bot = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Пользователь ВКонтакте"
        verbose_name_plural = "Пользователи ВКонтакте"
        ordering = ["user_id"]

    def __str__(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name


class VkEvent(models.Model):
    message_id = models.BigIntegerField(
        verbose_name="id сообщения ВКонтакте",
        help_text="id сообщения ВКонтакте",
        primary_key=True
    )
    from_user = models.ForeignKey(
        to=VkUser, on_delete=models.CASCADE, related_name="from_user",
        verbose_name="От кого",
        help_text="От кого"
    )
    to_user = models.ForeignKey(
        to=VkUser, on_delete=models.CASCADE, related_name="to_user",
        verbose_name="Кому",
        help_text="Кому"
    )
    date = models.DateTimeField(
        verbose_name="Время отправки",
        help_text="Время отправки",
        auto_now_add=True,
        blank=True
    )
    text = models.TextField(verbose_name="Текст сообщения", help_text="Текст сообщения")

    class Meta:
        verbose_name = "Событие ВКонтакте"
        verbose_name_plural = "События ВКонтакте"
        ordering = ["date"]
