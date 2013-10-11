import urllib2

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings

from .settings import HTTPS_IFRAME_COOKIESETTER_LOADING_GRAPHIC

def cookiesetter(request):
    quoted_absurl = request.GET.get('absurl', '/')
    absurl = urllib2.unquote(request.GET.get('absurl', '/'))
    fixed = request.GET.get('cookiefix', 'false')
    cookiesetter_view_path = reverse('cookiesetter', urlconf=django_settings.ROOT_URLCONF)

    return render_to_response('cookiesetter.html',{
            "redirect": (absurl!=cookiesetter_view_path),
            "current_url": request.build_absolute_uri().encode("utf8"),
            "cookiesetter_url": cookiesetter_view_path,
            "cookie_fixed": fixed =='true',
            "cookies": request.COOKIES,
            "absurl": absurl,
            "quoted_absurl": quoted_absurl,
            "loading_graphic" : HTTPS_IFRAME_COOKIESETTER_LOADING_GRAPHIC
            }, context_instance=RequestContext(request))