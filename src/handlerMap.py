#{%block imports%}
from Controllers import BaseControllers
from Controllers import StaticControllers
from Controllers import DictControllers
from Controllers import ShellControllers
from Controllers import ArmanListingControllers
from Controllers import CMSControllers
from Controllers import testModule
from Controllers import BordjControllers
#{%endblock%}
webapphandlers = [
#{%block ApplicationControllers %}
#{% block DictControllers %}
('/', DictControllers.SearchController),
('/dict/Word', DictControllers.WordController),
('/dict/Importer', DictControllers.ImporterController),
('/dict/Language', DictControllers.LanguageController),
('/dict/Dictionary', DictControllers.DictionaryController),
('/dict/WordSugestion', DictControllers.WordSugestionController),
#{%endblock%}
#{% block BordjControllers %}
('/Bordj', BordjControllers.DolgController),
#{%endblock%}

#{%block BaseControllers %}
('/Login', BaseControllers.LoginController),
('/Login/(.*)', BaseControllers.LoginController),
('/Logout',BaseControllers.LogoutController),
('/AddUser', BaseControllers.AddUserController),
('/WishList', BaseControllers.WishListController),
('/admin/Role', BaseControllers.RoleController),
('/admin/RoleAssociation', BaseControllers.RoleAssociationController),
('/Base/WishList', BaseControllers.WishListController),
('/Base/Invitation', BaseControllers.InvitationController),
#{%endblock%}

#{%block StaticControllers%}
('/Contact', StaticControllers.ContactController),
('/About', StaticControllers.AboutController),
('/Links', StaticControllers.LinksController),
('/NotAuthorized', StaticControllers.NotAuthorizedController),
#{%endblock%}

#{%block ArmanListingControllers %}
('/listing/Armans', ArmanListingControllers.ArmanController),
('/listing/Arman/Address', ArmanListingControllers.AddressController),
('/listing/Armans/Search', ArmanListingControllers.ArmanSearchController),
#{%endblock%}

#{%block ShellControllers%}
('/admin/Shell', ShellControllers.FrontPageController),
('/admin/stat.do', ShellControllers.StatementController),
#{%endblock%}

#{%block CMSControllers}
('/cms/content', CMSControllers.CMSContentController),
('/cms/content/(.*)', CMSControllers.CMSContentController),
('/cms/links', CMSControllers.CMSLinksController),
('/cms/page/(.*)/comment', CMSControllers.CommentController.new_factory(**{'op':'save'})),
('/cms/page/(.*)/comments', CMSControllers.CommentController.new_factory(**{'op':'index'})),
('/cms/page/(.*)', CMSControllers.CMSPageController),
#{%endblock%}
#{%block TestModuleControllers%)
('/test/1', testModule.TestHandler),
#{%endblock%}
('/(.*)', StaticControllers.NotExistsController),
]
#{%endblock%}