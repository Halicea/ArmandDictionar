# -*- coding: utf-8 -*-
import os
import settings
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.gaesessions import SessionMiddleware

#{% block imports %}
from Controllers import BaseControllers
from Controllers import StaticControllers
from Controllers import DictControllers
#{%endblock%}

#Definition of the Controller Url mappings
application = webapp.WSGIApplication(
[
#{% block ApplicationControllers %}

#{% block DictControllers %}
('/', DictControllers.SearchController),
('/Dict/Word', DictControllers.WordController),
('/Dict/Importer', DictControllers.ImporterController),
('/Dict/Language', DictControllers.LanguageController),
('/Dict/Dictionary', DictControllers.DictionaryController),
('/Dict/WordSugestion', DictControllers.WordSugestionController),
#{%endblock%}

#{% block BaseControllers %}
('/Login', BaseControllers.LoginController),
('/Logout',BaseControllers.LogoutController),
('/AddUser', BaseControllers.AddUserController),
('/WishList', BaseControllers.WishListController),
('/admin/Role', BaseControllers.RoleController),
('/admin/RoleAssociation', BaseControllers.RoleAssociationController),
('/Base/WishList', BaseControllers.WishListController),
#{%endblock%}

#{%block StaticControllers%}
('/Contact', StaticControllers.ContactController),
('/About', StaticControllers.AboutController),
('/Links', StaticControllers.LinksController),
('/NotAuthorized', StaticControllers.NotAuthorizedController),
#{%endblock%}


#{%endblock%}
('/(.*)', StaticControllers.NotExistsController),
], debug=settings.DEBUG)
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
