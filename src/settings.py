import os
from os.path import join
#from lib.halicea import defaultControllerMethods as dcm
from lib.halicea import dummyControllerMethods as dcm
DEBUG = False
TEMPLATE_DEBUG = True
DEFAULT_CHARSET ='UTF-8'
APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
if os.name == 'nt':
    #APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
    APPENGINE_PATH = 'C:\\devApps\\google_appengine'

#we define the path relatively to our settings file
PROJ_LOC = os.path.dirname(__file__)

#MVC Directories
MODELS_DIR = join(PROJ_LOC,'Models')
VIEWS_DIR = join(PROJ_LOC,'Views')
VIEWS_RELATIVE_DIR = ''
FORM_MODELS_DIR = join(PROJ_LOC, 'Forms')
CONTROLLERS_DIR = join(PROJ_LOC, 'Controllers')
BASE_VIEWS_DIR = join(VIEWS_DIR, 'bases')
BLOCK_VIEWS_DIR = join(VIEWS_DIR, 'blocks')
PAGE_VIEWS_DIR = join(VIEWS_DIR, 'pages')
FORM_VIEWS_DIR = join(VIEWS_DIR, 'forms')
STATIC_DATA_DIR = join(PROJ_LOC, 'StaticData')
JSCRIPTS_DIR = join(STATIC_DATA_DIR, 'jscripts')
IMAGES_DIR = join(STATIC_DATA_DIR, 'images')
STYLES_DIR = join(STATIC_DATA_DIR, 'styles')
HANDLER_MAP_FILE = join(PROJ_LOC, 'handlerMap.py')
#End MVC Directories

#MVC Sufixes
MODEL_MODULE_SUFIX = 'Models'
MODEL_FORM_MODULE_SUFIX = 'Forms'
CONTROLLER_MODULE_SUFIX = 'Controllers'
MODEL_CLASS_SUFIX = ''
MODEL_FORM_CLASS_SUFIX = 'Form'
CONTROLLER_CLASS_SUFIX = 'Controller'
BASE_VIEW_SUFIX = ''
PAGE_VIEW_SUFFIX = ''
FORM_VIEW_SUFFIX = 'Form'
BLOCK_VIEW_SUFIX = ''
#End MVC Sufixes


#File Extensions
CONTROLLER_EXTENSTION = '.py'
MODEL_EXTENSTION = '.py'
MODEL_FORM_EXTENSTION = '.py'
VIEW_EXTENSTION = '.html'

MagicLevel = 0

DEFAULT_OPERATIONS = {
                      'default':{'method':dcm.index, 'view':False},
                      'index':{'method':dcm.index, 'view':True}, 
                      'details':{'method':dcm.details, 'view':True},
                      'edit':{'method':dcm.edit, 'view':True},
                      'insert':{'method':dcm.save, 'view':False},
                      'update':{'method':dcm.save, 'view':False},
                      'delete':{'method':dcm.delete, 'view':False},
                     }
OPENID_PROVIDERS ={
    'Google':'Google.com/accounts/o8/id', # shorter alternative: "Gmail.com"
    'Yahoo':'Yahoo.com',
    #'MySpace.com',
    'MyOpenID':'MyOpenID.com',
    # add more here
}
#DJANGO APP SETTINGS SECTION
TEMPLATE_DIRS = (VIEWS_DIR)
ROOT_URLCONF ='handlerMap'
#PASTE YOUR CONFIGURATION HERE