import hashlib

from django.conf import settings


def md5(password):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(password.encode('utf-8'))
    return obj.hexdigest()
