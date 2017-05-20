"""
WSGI config for terrain project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
print('os')
from django.core.wsgi import get_wsgi_application
print('b')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "terrain.settings")
print('c')
application = get_wsgi_application()
print('d')
