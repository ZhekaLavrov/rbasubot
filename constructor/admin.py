from django.contrib import admin
from .models import Message, Button, Trigger, TelegramUser, TelegramMessage, CallBack


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    list_display_links = ("id", "text")
    search_fields = ("text", )


class ButtonAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "link", "message")
    list_display_links = ("id", "text", "link", "message")
    search_fields = ("text", "link")


class TriggerAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "button", "message", "next_message")
    list_display_links = ("id", "text", "button", "message", "next_message")
    search_fields = ("text", )


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "first_name",
        "last_name",
        "username",
        "is_bot",
    )
    list_display_links = (
        "user_id",
        "first_name",
        "last_name",
        "username",
    )
    search_fields = (
        "user_id",
        "first_name",
        "last_name",
        "username",
    )


class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = (
        "message_id",
        "from_user",
        "chat",
        "date",
        "text"
    )
    list_display_links = (
        "message_id",
        "date",
        "from_user",
        "chat",
        "text"
    )
    search_fields = ("text", )


class CallBackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "calldata",
        "from_user",
        "chat",
        "date",
        "message",
    )
    list_display_links = (
        "id",
        "calldata",
        "from_user",
        "chat",
        "date",
        "message",
    )
    search_fields = ("calldata", "message")


admin.site.register(Message, MessageAdmin)
admin.site.register(Button, ButtonAdmin)
admin.site.register(Trigger, TriggerAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramMessage, TelegramMessageAdmin)
admin.site.register(CallBack, CallBackAdmin)
