# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
import urllib2

def cookiesetter(request):
    absurl = request.GET.get('absurl', '/')
    return render_to_response('cookiesetter.html',{
            "absurl":urllib2.unquote(absurl)
            }, context_instance=RequestContext(request))