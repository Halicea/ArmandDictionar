#{%block imports%}
from Controllers import BaseControllers
from Controllers import StaticControllers
from Controllers import DictControllers
from Controllers import ShellControllers
from Controllers import ArmanListingControllers
from Controllers import BordjControllers
from Controllers import LWConnectControllers
from Controllers import stavControllers
from Controllers import testingControllers
#{%endblock%}

webapphandlers = [
#{%block ApplicationControllers %}
#{% block DictControllers %}
('/Search', DictControllers.SearchController),
('/Dict/Word', DictControllers.WordController),
('/Dict/Importer', DictControllers.ImporterController),
('/Dict/Language', DictControllers.LanguageController),
('/Dict/Dictionary', DictControllers.DictionaryController),
('/Dict/WordSugestion', DictControllers.WordSugestionController),
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
('/Listing/Armans', ArmanListingControllers.ArmanController),
('/Listing/Arman/Address', ArmanListingControllers.AddressController),
('/Listing/Armans/Search', ArmanListingControllers.ArmanSearchController),
#{%endblock%}
#{%block BordjContorlles%}
('/Bordj', BordjControllers.DolgController),
('/', BordjControllers.DolgController),
#{%endblock%}
#{%block ShellControllers%}
('/admin/Shell', ShellControllers.FrontPageController),
('/admin/stat.do', ShellControllers.StatementController),
#{%endblock%}

#{%block LWConnectControllers%}
('/LWConnect', LWConnectControllers.SprintController),
('/LWConnect/Branch', LWConnectControllers.BranchController),
('/LWConnect/ActivityLog', LWConnectControllers.ActivityLogController),
#('/LWConnect/test', LWConnectControllers.TestController),
#{%endblock%}
#{%block stavControllers%}
('/stav/Rabotnik', stavControllers.RabotnikController),
('/stav/Rezija', stavControllers.RezijaController),
('/stav/Nalog', stavControllers.NalogController),
('/stav/Partija', stavControllers.PartijaController),
('/stav/Rabota', stavControllers.RabotaController),
('/stav/Operacija', stavControllers.OperacijaController),
('/stav', stavControllers.PlataZaMesecController),
('/stav/(.*)', stavControllers.PlataZaMesecController),
#{%endblock%}
#{%block testingControllers%}
('/testing', testingControllers.testingController),
#{%endblock%}
#{%endblock%}
('/(.*)', StaticControllers.NotExistsController),
]

