# -*- coding: utf-8 -*-
import os 
import settings 
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.2')
from handlerMap import webapphandlers
from google.appengine.ext import webapp
import re
from google.appengine.ext.remote_api import handler
from google.appengine.ext.webapp.util import run_wsgi_app
#from lib import webapp2 as webapp
from lib.gaesessions import SessionMiddleware

#### Custom Remote Api Handler because of the OpenIdAuthentication
MY_SECRET_KEY = 'topsecret'
cookie_re = re.compile('^"([^:]+):.*"$')
class ApiCallHandler(handler.ApiCallHandler):
    def CheckIsAdmin(self):
        login_cookie = self.request.cookies.get('dev_appserver_login', '')
        match = cookie_re.search(login_cookie)
        if (match and match.group(1) == MY_SECRET_KEY
            and 'X-appcfg-api-version' in self.request.headers):
            return True
        else:
            self.redirect('/_ah/login')
            return False
webapphandlers2= webapphandlers#+[('*.',ApiCallHandler)]
#### End Custom Remote Api Handler because of the OpenIdAuthentication

application = webapp.WSGIApplication(webapphandlers2, debug=settings.DEBUG)

COOKIE_KEY = '''2zÆœ;¾±þ”¡j:ÁõkçŸÐ÷8{»Ën¿A—jÎžQAQqõ"bøó÷*%†™ù¹b¦$vš¡¾4ÇŸ^ñ5¦'''
def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app

def main():
    run_wsgi_app(webapp_add_wsgi_middleware(application))

if __name__ == "__main__":
    main()
