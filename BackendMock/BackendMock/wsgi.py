"""
WSGI config for BackendMock project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import django.conf
from django.core.wsgi import get_wsgi_application

django.conf.ENVIRONMENT_VARIABLE = "DJANGO_MOCKER_SETTING_MODULE"
os.environ.setdefault("DJANGO_MOCKER_SETTING_MODULE", "BackendMock.settings")

application = get_wsgi_application()
