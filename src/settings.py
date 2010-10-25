import os
from os.path import join, basename, abspath
DEBUG = True
TEMPLATE_DEBUG = True
DEFAULT_CHARSET ='UTF-8'
#APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
APPENGINE_PATH = 'C:\\devApps\\google_appengine'
TEMPLATE_DIRS = (abspath('Views'), 
                 abspath('Templates'),)

#Directory Structure
MODEL_MODULE_SUFIX = 'Models'
MODEL_CLASS_SUFIX = ''
CONTROLLER_MODULE_SUFIX = 'Controllers'
CONTROLLER_CLASS_SUFIX = 'Controller'

MODELS_DIR = abspath('Models')
VIEWS_DIR = abspath('Views')
CONTROLLERS_DIR = abspath('Controllers')

BASE_VIEWS_DIR = join(VIEWS_DIR, 'bases')
BASE_VIEW_SUFIX = ''
BLOCK_VIEWS_DIR = join(VIEWS_DIR, 'blocks')
BLOCK_VIEW_SUFIX = ''
PAGE_VIEWS_DIR = join(VIEWS_DIR, 'pages')
PAGE_VIEW_SUFFIX = ''
FORM_VIEWS_DIR = join(VIEWS_DIR, 'forms')
FORM_VIEW_SUFFIX = 'Form'

#End Directory Structure
#{Operation_ShortCut:{method:Controller_Method, view:Whether_it_Creates_View_or_No}}
DEFAULT_OPERATIONS = {'lst':{'method':'list', 'view':True}, 
                      'shw':{'method':'show', 'view':True},
                      'ins':{'method':'insert', 'view':False},
                      'upd':{'method':'insert', 'view':False},
                      'del':{'method':'delete', 'view':False},
                      'default':{'method':'show', 'view':False},
                     }

HANDLER_MAP_FILE = 'handlerMap.py'
