from django.shortcuts import render

from constructor.models import Message, Button, Trigger


def index(request):
    messages = Message.objects.all().order_by("id")
    return render(request, 'constructor/index.html', {"messages": messages})


def message(request, message_id):
    msg = Message.objects.filter(id=message_id)[:1]
    buttons = []
    triggers = []
    message_next_message = None
    buttons_next_buttons = []
    if len(msg):
        msg = msg[0]
        buttons = Button.objects.filter(message=msg)
        triggers = Trigger.objects.filter(next_message=msg)
        message_next_message = Trigger.objects.filter(message=msg)[:1]
        message_next_message = message_next_message[0] if len(message_next_message) else None
        buttons_next_buttons = [Trigger.objects.filter(button=button)[:1] for button in buttons]
    return render(
        request,
        'constructor/message.html',
        {
            "message": msg,
            "buttons": buttons,
            "triggers": triggers,
            "message_next_message": message_next_message,
            "buttons_next_buttons": buttons_next_buttons,
        }
    )
