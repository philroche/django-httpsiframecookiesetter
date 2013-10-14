import logging

from django.http import HttpResponseRedirect

from .utils import check_csrf_cookie_present

logger = logging.getLogger(__name__)

#If using a decorator then the middleware is not required
def check_csrf(view_func):
    """ Redirects to https:// version of URL (if not already secure and not DEBUG). """
    def _check_csrf(request, *args, **kwargs):
        cookie_present, redirect_url = check_csrf_cookie_present(request)
        if not cookie_present:
            return HttpResponseRedirect(redirect_url)
        else:
            return view_func(request, *args, **kwargs)
    return _check_csrf
