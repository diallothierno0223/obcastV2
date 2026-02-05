import os
import sys
from django.core.wsgi import get_wsgi_application

# On récupère le chemin du dossier racine (où se trouve manage.py)
# C'est-à-dire le parent du dossier actuel
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# On définit le module de settings
# Ici, on pointe sur le dossier de config interne
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
app = application