#coding: utf-8
import logging

from django.http import HttpResponseRedirect

from .utils import check_cookie_present


logger = logging.getLogger(__name__)

class CookieSetterMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(CookieSetterMiddleware, self).__init__(*args, **kwargs)


    def process_request(self, request):
        cookie_present, redirect_url = check_cookie_present(request)
        if not cookie_present:
            return HttpResponseRedirect(redirect_url)


