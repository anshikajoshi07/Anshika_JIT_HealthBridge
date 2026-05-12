"""
WSGI config for healthcare project.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')

from django.conf import settings

db_path = settings.DATABASES['default']['NAME']
print(f"STARTUP: DATABASE PATH = {db_path}")
print(f"STARTUP: DATABASE DIRECTORY EXISTS = {os.path.isdir(os.path.dirname(db_path))}")
print(f"STARTUP: DATABASE FILE EXISTS = {os.path.exists(db_path)}")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
