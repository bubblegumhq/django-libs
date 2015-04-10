from logging import getLogger
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import re

SSL = 'SSL'
LOGGER = getLogger(__name__)

class SSLRedirect:
    urls = tuple([re.compile(url) for url in settings.SSL_URLS])
    
    def process_request(self, request):
        LOGGER.info("SSL redirect")
        LOGGER.info(request.META.items())
        secure = False
        for url in self.urls:
            if url.match(request.path):
                secure = True
                LOGGER.info("URL '%s' need to be SECURE", request.path)
                break
        if secure != self._is_secure(request):
            LOGGER.info("Redirecting secure='%s",secure)
            return self._redirect(request, secure)

    def _is_secure(self, request):
        if request.is_secure():
            LOGGER.info("Request is already secure")
            return True

        #Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            LOGGER.info("HTTP_X_FORWARDED_SSL is in META")
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        return False

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        if secure:
            host = getattr(settings, 'SSL_HOST', request.get_host())
        else:
            host = getattr(settings, 'HTTP_HOST', request.get_host())
        newurl = "%s://%s%s" % (protocol,host,request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError, \
        """Django can't perform a SSL redirect while maintaining POST data.
           Please structure your views so that redirects only occur during GETs."""

        return HttpResponseRedirect(newurl)

class BasicAuthMiddleware(object):


    def unauthed(self):
        response = HttpResponse("""<html><title>Auth required</title><body>
                                <h1>Authorization Required</h1></body></html>""", mimetype="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response

    def process_request(self,request):
        if not request.META.has_key('HTTP_AUTHORIZATION'):

            return self.unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ',1)
            if 'basic' != authmeth.lower():
                return self.unauthed()
            auth = auth.strip().decode('base64')
            username, password = auth.split(':',1)
            if username == settings.BASICAUTH_USERNAME and password == settings.BASICAUTH_PASSWORD:
                return None

            return self.unauthed()


class CloudFlareCountryStoreMiddleware(object):


    def process_request(self,request):
        if request.META.has_key('HTTP_CF_IPCOUNTRY'):
            if hasattr(settings, "USER_COUNTRY_FIELD") and request.user.is_authenticated():
                country = request.META.get('HTTP_CF_IPCOUNTRY')
                LOGGER.info(u"Setting country of %s on user with email %s" % (country, request.user.email))
                setattr(request.user, settings.USER_COUNTRY_FIELD, country)
                request.user.save()

class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)