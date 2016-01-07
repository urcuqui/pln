"""
WSGI config for pln project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/pln/local/lib/python2.7/site-packages')


from django.core.wsgi import get_wsgi_application

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/pln')
sys.path.append('/var/www/pln/pln')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pln.settings")

# Activate your virtual env
activate_env=os.path.expanduser("/home/i2t/.virtualenvs/pln/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

application = get_wsgi_application()