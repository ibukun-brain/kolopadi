"""
WSGI config for kolopadi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from kolopadi.settings import base_settings

if base_settings.DEBUG:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "kolopadi.settings.development_settings"
    )

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "kolopadi.settings.production_settings"
)

application = get_wsgi_application()

app = application
