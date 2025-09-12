from django.urls import path
from slackintegration import views

urlpatterns = [
    path("api/send-message/", views.send_message_api, name="send-message"),
]