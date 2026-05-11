"""
WSGI config for healthcare project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')

print('Startup log: Django DB path = /var/data/db.sqlite3')

application = get_wsgi_application()
