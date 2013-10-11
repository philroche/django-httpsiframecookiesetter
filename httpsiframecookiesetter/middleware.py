#coding: utf-8

import logging
import urllib2
from user_agents import parse
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf import settings as django_settings
from django.middleware.csrf import _sanitize_token
from django.core.urlresolvers import reverse


from .settings import HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK, HTTPS_IFRAME_COOKIESETTER_BROWSERS, \
                        HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS, HTTPS_IFRAME_COOKIESETTER_ONLY_HTTPS


logger = logging.getLogger(__name__)

class CookieSetterMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(CookieSetterMiddleware, self).__init__(*args, **kwargs)
        self._property_cache = {}

    def call_additional_checks(self):
        #a result of True means that it passes a check - the default is that there is no check so returns True
        result = True
        if(HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS is not None and hasattr(HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS, '__call__')):
            result = HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS()
        return True

    def urlpath(self):
        if not self._property_cache.has_key('cookiesetter_view_path'):
            self._property_cache['cookiesetter_view_path'] = reverse('cookiesetter', urlconf=django_settings.ROOT_URLCONF)
        return self._property_cache['cookiesetter_view_path']

    def process_request(self, request):

        #TODO we need to check the number of redirects in case we end up in a loop for some reason
        if (not HTTPS_IFRAME_COOKIESETTER_ONLY_HTTPS or(HTTPS_IFRAME_COOKIESETTER_ONLY_HTTPS and request.is_secure())) \
            and not (request.path.startswith(settings.MEDIA_URL) or request.path.startswith(settings.STATIC_URL)) \
            and  HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK in request.path \
            and self.call_additional_checks():
            #get the url to the cookiesetter view
            cookiesetter_view_path = self.urlpath()
            user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))

            if user_agent.browser.family in HTTPS_IFRAME_COOKIESETTER_BROWSERS \
                and cookiesetter_view_path not in request.path:#these are after the initial check as it is an expensive lookup

                current_absolute_url = urllib2.quote(request.build_absolute_uri().encode("utf8"))
                csrf_token = None

                try:
                    csrf_token = _sanitize_token(request.COOKIES[settings.CSRF_COOKIE_NAME])
                except KeyError:
                    csrf_token = None

                if not csrf_token:
                    #ehck url scheme to http
                    redirect_url = '%s?absurl=%s' %(cookiesetter_view_path, current_absolute_url)
                    redirect_url = request.build_absolute_uri(redirect_url)
                    parsed = urlparse(redirect_url)
                    redirect_url = '%s://%s%s?%s' % ('http',parsed.netloc, parsed.path, parsed.query)
                    return HttpResponseRedirect(redirect_url)

