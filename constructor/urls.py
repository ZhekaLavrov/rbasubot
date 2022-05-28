from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('message/<int:message_id>', views.message)
]

