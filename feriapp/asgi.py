"""Punto de entrada ASGI para ejecuciones asíncronas del proyecto."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feriapp.settings")

application = get_asgi_application()
