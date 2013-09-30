from django.conf import settings

HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK = getattr(settings, 'COOKIESETTER_URL_TO_CHECK', '/myview')