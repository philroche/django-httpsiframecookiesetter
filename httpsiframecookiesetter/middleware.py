#coding: utf-8

import logging

from django.conf import settings
from django.http import HttpResponseRedirect

from django.conf import settings
from django.middleware.csrf import _sanitize_token
from django.core.urlresolvers import reverse
import urllib2

from .settings import HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK


logger = logging.getLogger(__name__)

class CookieSetterMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(CookieSetterMiddleware, self).__init__(*args, **kwargs)
        self._property_cache = {}

    def urlpath(self):
        if not self._property_cache.has_key('cookiesetter_view_path'):
            cookiesetter_view_path = reverse('cookiesetter', urlconf=settings.ROOT_URLCONF)
            self._property_cache['cookiesetter_view_path'] = cookiesetter_view_path
        return self._property_cache['cookiesetter_view_path']

    def clear_property_cache(self):
        self._property_cache = {}

    def process_request(self, request):

        #TODO - use browser sniffer
        #TODO - use check safari, csrf and is_secure, an iframe first so it is only safari that is slowed down
        #get the url to the cookiesetter view
        #cached value
        cookiesetter_view_path = self.urlpath()


        #TODO we need to check the number of redirects in case we end up in a loop for some reason
        if request.is_secure() and not (request.path.startswith(settings.MEDIA_URL) or request.path.startswith(settings.STATIC_URL)) and cookiesetter_view_path not in request.path and HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK in request.path:
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            browser_is_safari = 'Safari' in user_agent and 'Chrome' not in user_agent
            current_absolute_url = urllib2.quote(request.build_absolute_uri().encode("utf8"))
            csrf_token = None

            try:
                csrf_token = _sanitize_token(request.COOKIES[settings.CSRF_COOKIE_NAME])
            except KeyError:
                csrf_token = None
            #
            if browser_is_safari and not csrf_token:
                return HttpResponseRedirect('%s?absurl=%s' %(reverse('cookiesetter', urlconf='urls'), current_absolute_url))

