from django.urls import path

from . import views

app_name = "postmark_incoming"
urlpatterns = [
    path("webhook/", views.webhook_view, name="webhook"),
]
