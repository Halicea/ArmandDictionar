import os
from os.path import join, basename, abspath
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
#Directory Structure
MODEL_MODULE_SUFIX = 'Models'
MODEL_CLASS_SUFIX = ''
CONTROLLER_MODULE_SUFIX = 'Controllers'
CONTROLLER_CLASS_SUFIX = 'Controller'

MODELS_DIR = join(PROJ_LOC,'Models')
VIEWS_DIR = join(PROJ_LOC,'Views')
CONTROLLERS_DIR = join(PROJ_LOC, 'Controllers')

BASE_VIEWS_DIR = join(VIEWS_DIR, 'bases')
BASE_VIEW_SUFIX = ''
BLOCK_VIEWS_DIR = join(VIEWS_DIR, 'blocks')
BLOCK_VIEW_SUFIX = ''
PAGE_VIEWS_DIR = join(VIEWS_DIR, 'pages')
PAGE_VIEW_SUFFIX = ''
FORM_VIEWS_DIR = join(VIEWS_DIR, 'forms')
FORM_VIEW_SUFFIX = 'Form'

STATIC_DATA_DIR = join(PROJ_LOC, 'StaticData')
JSCRIPTS_DIR = join(STATIC_DATA_DIR, 'jscripts')
IMAGES_DIR = join(STATIC_DATA_DIR, 'images')
STYLES_DIR = join(STATIC_DATA_DIR, 'styles')

HANDLER_MAP_FILE = join(PROJ_LOC, 'handlerMap.py')
#End Directory Structure
#{Operation_ShortCut:{method:Controller_Method, view:Whether_it_Creates_View_or_No}}
DEFAULT_OPERATIONS = {'lst':{'method':'list', 'view':True}, 
                      'shw':{'method':'show', 'view':True},
                      'ins':{'method':'insert', 'view':False},
                      'upd':{'method':'insert', 'view':False},
                      'del':{'method':'delete', 'view':False},
                      'default':{'method':'show', 'view':False},
                     }
