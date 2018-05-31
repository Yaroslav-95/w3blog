from . import apps
from django.conf import settings

if settings.WEBLOG_SETTINGS:
    for key, value in settings.WEBLOG_SETTINGS.items():
        apps.SETTINGS[key] = value
