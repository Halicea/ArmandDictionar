import os
import sys
from os.path import join as pjoin
from os.path import abspath, dirname, basename
APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
if os.name == 'nt':
    #PPENGINE_PATH = 'C:\\Users\\Costa\\Appengine'
    APPENGINE_PATH = 'C:\\DevApps\\google_appengine'
elif sys.platform=='darwin':
    APPENGINE_PATH = '/Users/costa/DevApps/google_appengine'
installPath = dirname(dirname(abspath(__file__)))
PROJ_LOC = pjoin(dirname(dirname(__file__)), 'src')
sys.path.append(abspath(pjoin(PROJ_LOC)))
#Set django in pythonpath
sys.path.append(APPENGINE_PATH)
sys.path.append(pjoin(APPENGINE_PATH, 'lib'))
sys.path.append(pjoin(APPENGINE_PATH, 'lib', 'django' ))
sys.path.append(pjoin(APPENGINE_PATH, 'lib', 'webob' ))
sys.path.append(pjoin(APPENGINE_PATH, 'lib', 'yaml','lib' ))
###
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from halicea import renderers
import settings as proj_settings

#default model Inherit
modelInheritsFrom = 'db.Model'
#default Controller inherit
controllerInheritsFrom = 'hrh'
#default Form inherit
formInheritsFrom = 'ModelForm'
#urlTemplate = '/$Package/$Model/$Action'
urlTemplate = '/$Package/$Model/?op=$Action'
#Template Renderer Configuration
TEMPLATE_RENDERER = renderers.Django
#Template Configuration
TMPL_DIR = pjoin(PROJ_LOC, os.sep.join(['Templates', 'WEBOBTemplates', '{{magicLevel}}']))
MvcTemplateDirs = \
    {
        'TMPLR_DIR'   : TMPL_DIR,
        'FRMTMPL_DIR' : pjoin(TMPL_DIR,'FormTemplates'),
        'OPRTMPL_DIR' : pjoin(TMPL_DIR,'OperationTemplates'),
        'MBTMPL_DIR'  : pjoin(TMPL_DIR,'ModuleBaseTemplates'),
    }
MvcTemplateFiles = \
    {
        'MTPath'  : pjoin(TMPL_DIR, 'ModelTemplate.txt'),
        'MBTPath' : pjoin(MvcTemplateDirs['MBTMPL_DIR'], 'ModelModule.txt'),
        
        'FTPath'  : pjoin(TMPL_DIR,'ModelFormTemplate.txt'),
        'FBTPath' : pjoin(MvcTemplateDirs['MBTMPL_DIR'], 'ModelFormModule.txt'),
        
        'VTPath'  : pjoin(TMPL_DIR,'ViewTemplate.txt'),
        'CTPath'  : pjoin(TMPL_DIR,'ControllerTemplate.txt'),
        'CBTPath' : pjoin(MvcTemplateDirs['MBTMPL_DIR'],'ControllerModule.txt'),
    }
mvcPaths = \
    {
        "modelsPath"    : basename(proj_settings.MODELS_DIR), 
        'viewsPath'     : basename(proj_settings.VIEWS_DIR), 
        'formsPath'     : basename(proj_settings.FORM_MODELS_DIR),
        'controlersPath': basename(proj_settings.CONTROLLERS_DIR),
    }
djangoVars = \
    {
        'ob' : '{{',
        'cb' : '}}',
        'os' : '{%',
        'cs' : '%}',
    }
sufixesDict = \
    {
        'CONTROLLER_CLASS_SUFIX'    : proj_settings.CONTROLLER_CLASS_SUFIX,
        'CONTROLLER_MODULE_SUFIX'   : proj_settings.CONTROLLER_MODULE_SUFIX,
        'MODEL_CLASS_SUFIX'         : proj_settings.MODEL_CLASS_SUFIX,
        'MODEL_MODULE_SUFIX'        : proj_settings.MODEL_MODULE_SUFIX,
        'FORM_VIEW_SUFFIX'          : proj_settings.FORM_VIEW_SUFFIX,
        'BLOCK_VIEW_SUFIX'          : proj_settings.BLOCK_VIEW_SUFIX, 
        'MODEL_FORM_CLASS_SUFIX'    : proj_settings.MODEL_FORM_CLASS_SUFIX,
        'MODEL_FORM_MODULE_SUFIX'   : proj_settings.MODEL_FORM_MODULE_SUFIX,
    }
types =\
    {
        'txt'       : 'db.TextProperty',
        'str'       : 'db.StringProperty',
        'blob'      : 'db.BlobProperty',
        'bln'       : 'db.BooleanProperty',
        'dtm'       : 'db.DateTimeProperty',
        'date'      : 'db.DateProperty',
        'time'      : 'db.TimeProperty',
        'email'     : 'db.EmailProperty',
        'int'       : 'db.IntegerProperty',
        'float'     : 'db.FloatProperty',
        'ref'       : 'db.ReferenceProperty',
        'selfref'   : 'db.SelfReferenceProperty',
        'list'      : 'db.ListProperty',
        'strlist'   : 'fb.StringListProperty',
        'cat'       : 'db.CategoryProperty',
        'link'      : 'db.LinkProperty',
        'im'        : 'db.IMProperty',
        'geopt'     : 'db.GeoPtProperty',
        'phone'     : 'db.PhoneNumberProperty',
        'postal'    : 'db.PostalAddressProperty',
        'rating'    : 'db.RatingProperty',
        'user'      : 'db.UserProperty',
    }

