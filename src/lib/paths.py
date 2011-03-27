'''
Created on 04.1.2010

@author: KMihajlov
'''
import os
import os.path as p
from os.path import join as pjoin
import settings
from google.appengine.api import memcache
os.path.sep = '/'
os.pathsep = '/'

def GetTemplateDir(template_type):
    # @type template_type:str
    return p.join(settings.PAGE_VIEWS_DIR, template_type)

def getViewsDict(dir, base=''):
    result = {}
    #memcached for better performance
    memResult = memcache.get('paths_ViewsDict_'+dir)
    if memResult is None:
        if os.path.exists(dir) and os.path.isdir(dir):
            for f in os.listdir(dir):
                rf = os.path.join(dir, f)
                if os.path.isfile(rf):
                    
                    result[f[:f.rindex('.')]] = os.path.abspath(rf)[base and base.length or 0:]
    else:
        memcache.add(key='paths_ViewsDict', value=result)
    return result

def GetBasesDict():
    result = getViewsDict(settings.BASE_VIEWS_DIR, settings.VIEWS_RELATIVE_DIR)
    return result

def GetBlocksDict():
    result = getViewsDict(settings.BLOCK_VIEWS_DIR, settings.VIEWS_RELATIVE_DIR)
    result.update(__blocksDict__)
    return result

def GetFormsDict(dir):
    result = getViewsDict(p.join(settings.FORM_VIEWS_DIR, dir), settings.VIEWS_RELATIVE_DIR)
    return result

__blocksDict__={
        "blLogin":          pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],'login_menu.inc.html'),
        "blLanguages":      pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],'dict_Languages.inc.html'),
        'blDictMenu':       pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],'menu.bl.inc.html'),
        "mnTopMenu":        pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],'top_menu.inc.html'),
        ### Menu Blocks
        "blAdminMenu":      pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],"menu_links/admin.inc.html"),
        "blLogedUserMenu":  pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],"menu_links/loged_user.inc.html"),
        "blDefaultMenu":    pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],"menu_links/default.inc.html"),
        'blMembersGadget':  pjoin(settings.BLOCK_VIEWS_DIR[len(settings.VIEWS_RELATIVE_DIR):],"google-ajax-api/members_gadget.html"),
        'blTransactionVerification': pjoin(settings.VIEWS_DIR,"mail_templates/transaction_verification.html")[len(settings.VIEWS_RELATIVE_DIR):],
        }

__pluginsDict__={
                 'plQuestionarySmall': {'path': '../../lib/plugins/questionaryPlugin',
                                        'view': 'questionaryView.html',
                                        'controller': '',
                                        },
                 }