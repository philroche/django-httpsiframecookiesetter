django-httpsiframecookiesetter
==============================

A workaround for Safari's strict cookie policy when trying to write cookies from within an iframe under https.

This fix is specific to Django and the CSRF cookie.

If your view is within an iframe and is secure then Safari does not permit you to write any cookies if you are not on the same domain as that of the parent page. This is a problem when using Django when trying to POST forms as the CSRF cookie can not be written and therefore Django will not process the POST request.

Solution
-----

When a specified URL is visited _and_ the request is secure _and_ there is no CSRF cookie then the user is redirected to a non secure view which sets the CSRF cookie (safari allows this) and then redirects back to the secure URL.

Usage
-----
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


You can also set the URL to check - only URLs containing '/events/' will be processed and also change other settings below

    #iframe cookie setter settings
    COOKIESETTER_URL_TO_CHECK = '/i/events/'
    COOKIESETTER_BROWSERS =  ['Safari','Mobile Safari']
    COOKIESETTER_ADDITIONAL_CHECKS =  None
    COOKIESETTER_ONLY_HTTPS = False
    COOKIESETTER_LOADING_GRAPHIC = '/media/img/ajaxloader75_32.gif'

If needed overwrite templates with your message and style. For reference look at source (download url).