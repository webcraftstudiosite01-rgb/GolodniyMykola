"""ASGI config for Django Premium Studio."""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects.settings')

application = get_asgi_application()
