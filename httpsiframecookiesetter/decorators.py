import logging

from django.http import HttpResponseRedirect

from .utils import check_cookie_present

logger = logging.getLogger(__name__)

#If using a decorator then the middleware is not required
def check_cookies_present(view_func):
    def _check_cookies_present(request, *args, **kwargs):
        cookie_present, redirect_url = check_cookie_present(request)
        if not cookie_present:
            return HttpResponseRedirect(redirect_url)
        else:
            return view_func(request, *args, **kwargs)
    return _check_cookies_present #_check_csrf
