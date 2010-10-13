'''
Created on 04.1.2010

@author: KMihajlov
'''
import os
import os.path as p
import settings

def GetTemplateDir(template_type):
    # @type template_type:str 
    return p.join(settings.PAGE_VIEWS_DIR, template_type)

def getViewsDict(dir):
    result = {}
    if os.path.exists(dir) and os.path.isdir(dir):
        for f in os.listdir(dir):
            rf = os.path.join(dir, f)
            if os.path.isfile(rf):
                result[f[:f.rindex('.')]] = os.path.abspath(rf)
    return result

def GetBasesDict():
    result = getViewsDict(settings.BASE_VIEWS_DIR)
    result.update(__basesDict__)
    return result

def GetBlocksDict():
    result = getViewsDict(settings.BLOCK_VIEWS_DIR)
    result.update(__blocksDict__)
    return result

def GetMenusDict():
    return __menusDict__

def GetPluginsDict():
    return __pluginsDict__

def GetLinks():
    pass
    
__basesDict__={
        "base":             "../../bases/base.html",
        "darkness_base":    "../../bases/darkness_base.html",
        }

__menusDict__={
       "mnTopMenu":         "../../blocks/top_menu.inc.html",
       }

__blocksDict__={
        "blLogin":          "../../blocks/login_menu.inc.html",
        "blLanguages":      "../../blocks/dict_Languages.inc.html",
        'blDictMenu':       "../../blocks/menu.bl.html",
        ### Menu Blocks
        "blAdminMenu":      "../../blocks/menu_links/admin.inc.html",
        "blLogedUserMenu":  "../../blocks/menu_links/loged_user.inc.html",
        "blDefaultMenu":    "../../blocks/menu_links/default.inc.html",
        'blMembersGadget':     "../../blocks/google-ajax-api/members_gadget.html",
        'blTransactionVerification': "../../mail_templates/transaction_verification.html",
        }

__pluginsDict__={
                 'plQuestionarySmall': {'path': '../../lib/plugins/questionaryPlugin',
                                        'view': 'questionaryView.html',
                                        'controller': '',
                                        },
                 }