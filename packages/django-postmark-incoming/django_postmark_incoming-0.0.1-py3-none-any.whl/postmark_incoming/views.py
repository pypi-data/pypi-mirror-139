import json
import logging
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from . import models

User = get_user_model()
logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def webhook_view(request):
    try:
        payload = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        return JsonResponse({"detail": "Invalid payload"}, status=400)

    headers = {}
    for key in request.headers:
        value = request.headers[key]
        if isinstance(value, str):
            headers[key] = value

    wh = models.PostmarkWebhook.objects.create(
        body=payload,
        headers=headers,
        status=models.PostmarkWebhook.Status.NEW,
    )
    logger.info(f"PostmarkWebhook.id={wh.id} webhook received")

    # TODO
    # if hasattr(tasks, "shared_task"):
    #     tasks.process_webhook.delay(wh.id)
    # else:
    #     tasks.process_webhook(wh.id)

    return JsonResponse({"detail": "Created"}, status=201)
