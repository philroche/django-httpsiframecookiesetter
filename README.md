django-httpsiframecookiesetter
==============================

A workaround for Safari's strict cookie policy when trying to write cookies from within an iframe under https

Usage
Add new midleware after session creation:
MIDDLEWARE_CLASSES = (
    ...
    'httpsiframecookiesetter.middleware.CookieSetterMiddleware',
    ...
)
add iframetoolbox to installed apps:
INSTALLED_APPS = (
    ...
    'httpsiframecookiesetter',
    ...
)
add url config:
url(r'^cookiesetter/', include('httpsiframecookiesetter.urls')),


You can also set the URL to check - only URLs containing '/events/' will be processed
#iframe cookie setter settings
COOKIESETTER_URL_TO_CHECK = '/events/'

If needed overwrite templates with your message and style. For reference look at source (download url).