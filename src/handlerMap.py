from django.conf.urls.defaults import *
#{%block imports%}
from Controllers import BaseControllers
from Controllers import StaticControllers
from Controllers import DictControllers
from Controllers import ShellControllers
from Controllers import ArmanListingControllers
from Controllers import ChatControllers
#{%endblock%}

webapphandlers = [
#{%block ApplicationControllers %}
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

#{%block ArmanListingControllers %}
('/Listing/Armans', ArmanListingControllers.ArmanController),
#{%endblock%}

#{%block ShellControllers%}
('/admin/Shell', ShellControllers.FrontPageController),
('/admin/stat.do', ShellControllers.StatementController),
#{%endblock%}

#{%block ChatControllers%}
('/Chat/User', ChatControllers.UserController),
('/Chat/Room', ChatControllers.RoomController),
('/Chat/UserInRoom', ChatControllers.UserInRoomController),
('/Chat/Message', ChatControllers.MessageController),
#{%endblock%}
('/(.*)', StaticControllers.NotExistsController),
#{%endblock%}
]
urlpatterns=patterns('',*[(r'^'+x[0][1:]+'$', x[1]) for x in webapphandlers])
