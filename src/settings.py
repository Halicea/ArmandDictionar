import os
from os.path import join, abspath
from lib.halicea import defaultControllerMethods as dcm
DEBUG = True
TEMPLATE_DEBUG = True
DEFAULT_CHARSET ='UTF-8'
APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
if os.name == 'nt':
    #APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
    APPENGINE_PATH = 'C:\\devApps\\google_appengine'
TEMPLATE_DIRS = (abspath('Views'), 
                 abspath('Templates'),)
#we define the path relatively to our settings file
PROJ_LOC = os.path.dirname(__file__)
#MVC Directories
MODELS_DIR = join(PROJ_LOC,'Models')
VIEWS_DIR = join(PROJ_LOC,'Views')
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
                      'lst':{'method':dcm.index, 'view':True}, 
                      'shw':{'method':dcm.show, 'view':True},
                      'ins':{'method':dcm.save, 'view':False},
                      'upd':{'method':dcm.save, 'view':False},
                      'del':{'method':dcm.delete, 'view':False},
                      'default':{'method':dcm.index, 'view':False},
                     }
#DJANGO APP SETTINGS SECTION
#PASTE YOUR CONFIGURATION HERE