from django.contrib import admin
from .models import Message, Button, Trigger, TelegramUser, TelegramMessage, CallBack

admin.site.register(Message)
admin.site.register(Button)
admin.site.register(Trigger)
admin.site.register(TelegramUser)
admin.site.register(TelegramMessage)
admin.site.register(CallBack)
