from django.conf.urls import patterns, url
from .views import cookiesetter

urlpatterns = patterns('',
    url(r'$', cookiesetter, name='cookiesetter'),
)