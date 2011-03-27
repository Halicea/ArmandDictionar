# -*- coding: utf-8 -*-
import os 
import settings 
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.2')
from handlerMap import webapphandlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
#from lib import webapp2 as webapp
from lib.gaesessions import SessionMiddleware

application = webapp.WSGIApplication(webapphandlers, debug=settings.DEBUG)

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
