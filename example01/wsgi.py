"""
WSGI config for example01 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.wsgi import get_wsgi_application

scheduler = BackgroundScheduler()


@scheduler.scheduled_job(trigger='interval', days=7, start_date="2024-7-25 9:05:00", id="clear session")
def clear_session_job():
    print('clear session data base')
    os.system('python manage.py clearsessions')


scheduler.start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example01.settings')

application = get_wsgi_application()
