# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.gaesessions import SessionMiddleware

# {% block imports %}
from Controllers import baseControllers
from Controllers import staticControllers
from Controllers import DictControllers
#from Controllers import TournamentHostControllers

# {% endblock %}

#"""Load custom Django template filters"""
#webapp.template.register_template_library('lib.customFilters')

debug=True
application = webapp.WSGIApplication(
[
 ##########
 #{% block ApplicationControllers %}
('/', DictControllers.SearchController),
('/Dict/Word', DictControllers.WordController),
('/Dict/Importer', DictControllers.ImporterController),
('/Dict/Language', DictControllers.LanguageController),
('/Dict/Dictionary', DictControllers.DictionaryController),
('/Dict/WordSugestion', DictControllers.WordSugestionController),

#('/Tournament/Info', TournamentHostControllers.TournamentInfoController),
#('/TournamentHost/Host', TournamentHostControllers.HostController),
#('/TournamentHost/Guest', TournamentHostControllers.GuestController),

('/Base/Role', baseControllers.RoleController),
('/Base/RoleAssociation', baseControllers.RoleAssociationController),
 #{% endblock %}
 #{% block baseControllers %}
 ('/Login', baseControllers.LoginController),
 ('/Logout', baseControllers.LogoutController),
 ('/AddUser', baseControllers.AddUserController),
 ('/WishList', baseControllers.WishListController),
 #{%endblock%}
 
 #{%block staticControllers%}
 ('/Contact', staticControllers.ContactController),
 ('/About', staticControllers.AboutController),
 ('/Links', staticControllers.LinksController),
 ('/NotAuthorized', staticControllers.NotAuthorizedController),
 #{%endblock%}
 #('/(.*)', staticControllers.NotExistsController),
], debug=debug)
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
