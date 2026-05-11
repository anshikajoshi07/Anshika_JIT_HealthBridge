"""
WSGI config for healthcare project.
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')

application = get_wsgi_application()

# Ensure the database is migrated when the WSGI app starts, especially on Render.
try:
    call_command('migrate', interactive=False, verbosity=0)
except Exception as e:
    print(f"WSGI migration error: {e}")
