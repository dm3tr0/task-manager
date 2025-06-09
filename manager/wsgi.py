import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from manager.settings import STATIC_ROOT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=STATIC_ROOT)

