from django.urls import path, include

urlpatterns = [
    path("postmark_incoming/webhook/", include("postmark_incoming.urls")),
]
