from django.urls import reverse

from .. import models


def test_create_webhook(client):
    """Create event"""
    url = reverse("postmark_incoming:webhook")
    payload = {"id": "evt_test", "object": "event", "type": "test"}
    response = client.post(url, payload, content_type="application/json")
    assert response.status_code == 201
    assert 1 == models.PostmarkWebhook.objects.count()


def test_bad_json(client):
    """Malformed JSON"""
    url = reverse("postmark_incoming:webhook")
    payload = "bad json"
    response = client.post(url, payload, content_type="application/json")
    assert response.status_code == 400
    assert models.PostmarkWebhook.objects.count() == 0
