from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.gaesessions import SessionMiddleware

# {% block imports %}
from Controllers import baseControllers
from Controllers import staticControllers
from Controllers import DictControllers
from Controllers import TournamentHostControllers
# {% endblock %}

#"""Load custom Django template filters"""
#webapp.template.register_template_library('lib.customFilters')

debug=True
application = webapp.WSGIApplication(
[
 ##########
('/', DictControllers.SearchController),
 #{% block ApplicationControllers %}
('/Dict/Word', DictControllers.WordController),
('/Dict/Importer', DictControllers.ImporterController),

('/Tournament/Info', TournamentHostControllers.TournamentInfoController),
('/TournamentHost/Host', TournamentHostControllers.HostController),
('/TournamentHost/Guest', TournamentHostControllers.GuestController),
('/Dict/Language', DictControllers.LanguageController),
('/Dict/Dictionary', DictControllers.DictionaryController),
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
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app)
    return app
def main():
	run_wsgi_app(\
					 webapp_add_wsgi_middleware(application)\
					)

if __name__ == "__main__":
	main()
