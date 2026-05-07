"""Punto de entrada WSGI para despliegues del proyecto."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feriapp.settings")
application = get_wsgi_application()
