import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

from blue_diamond_research.settings.base import dotenv_path

load_dotenv(dotenv_path)
django_settings_module_path = os.environ.get("DJANGO_SETTINGS_MODULE")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module_path)

application = get_wsgi_application()
