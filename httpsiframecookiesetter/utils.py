import urllib2
import logging
from user_agents import parse
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.conf import settings

from django.conf import settings as django_settings
from django.core.urlresolvers import reverse


from .settings import HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK, HTTPS_IFRAME_COOKIESETTER_BROWSERS, \
                        HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS, HTTPS_IFRAME_COOKIESETTER_ONLY_HTTPS, \
                        HTTPS_IFRAME_COOKIESETTER_COOKIES

_property_cache = {}

logger = logging.getLogger(__name__)

def call_additional_checks():
    #a result of True means that it passes a check - the default is that there is no check so returns True
    result = True
    if(HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS is not None and hasattr(HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS, '__call__')):
        result = HTTPS_IFRAME_COOKIESETTER_ADDITIONAL_CHECKS()
    return True

def urlpath():
    if not _property_cache.has_key('cookiesetter_view_path'):
        _property_cache['cookiesetter_view_path'] = reverse('cookiesetter', urlconf=django_settings.ROOT_URLCONF)
    return _property_cache['cookiesetter_view_path']


def check_cookie_present(request):
    #TODO we need to check the number of redirects in case we end up in a loop for some reason
    if  HTTPS_IFRAME_COOKIESETTER_URL_TO_CHECK in request.path \
        and not (request.path.startswith(settings.MEDIA_URL) or request.path.startswith(settings.STATIC_URL)) \
        and (not HTTPS_IFRAME_COOKIESETTER_ONLY_HTTPS or(HTTPS_IFRAME_COOKIESETTER_ONLY_HTTPS and request.is_secure())) \
        and call_additional_checks():
        #get the url to the cookiesetter view
        cookiesetter_view_path = urlpath()
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))

        if user_agent.browser.family in HTTPS_IFRAME_COOKIESETTER_BROWSERS \
            and cookiesetter_view_path not in request.path:#these are after the initial check as it is an expensive lookup

            current_absolute_url = urllib2.quote(request.build_absolute_uri().encode("utf8"))

            cookies_present = True

            for cookie_string in HTTPS_IFRAME_COOKIESETTER_COOKIES:
                try:
                    cookie_token = request.COOKIES[cookie_string]
                except KeyError:
                    cookies_present = False

            if not cookies_present:
                #ehck url scheme to http
                redirect_url = '%s?absurl=%s' %(cookiesetter_view_path, current_absolute_url)
                redirect_url = request.build_absolute_uri(redirect_url)
                parsed = urlparse(redirect_url)
                redirect_url = '%s://%s%s?%s' % ('http',parsed.netloc, parsed.path, parsed.query)
                return False,redirect_url


    requested_url = request.build_absolute_uri()
    return True, requested_url