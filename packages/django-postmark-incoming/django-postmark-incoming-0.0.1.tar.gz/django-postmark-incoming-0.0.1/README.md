# django-postmark-incoming

Django conveniences for Postmark incoming emails. Incoming emails are stored in the `IncomingEmail` model. Use signals in other apps to detect new emails.

## TODO
- Processing of Webhook
- Add Usage section that directs you to add the webhook path in Postmark
## Installation


1. Add "django-postmark-incoming" to your `requirements.txt`
1. You may now need to install it with `pip install -r requirements.txt`.
1. Add "postmark_incoming" to your INSTALLED_APPS setting like this:
   ```
   INSTALLED_APPS = [
       ...
       "postmark_incoming",
       ...
   ]
   ```
1. Include the postmark_incoming URLconf in your project urls.py like this:
   ```
       path('postmark_incoming/', include('postmark_incoming.urls')), 
   ```
1. OPTIONAL: Use celery for webhook processing: `pip install celery` and add it to requirements. If you don't install celery, it will process webhooks synchronously.
1. Run `python manage.py migrate` to create the models.

## Running the Test Suite

1. `python3 -m venv .venv`
1. `source .venv/bin/activate`
1. `pip install -r requirements.txt`
1. `py.test`

## Releases

To publish a new release, push a git tag.