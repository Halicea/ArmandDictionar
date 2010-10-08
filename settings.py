import os

DEBUG = True
TEMPLATE_DEBUG = True
APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
#APPENGINE_PATH = '/home/costa/DevApps/google_appengine/'
TEMPLATE_DIRS = (os.path.abspath('Views'), 
                 os.path.abspath('Templates'),)
DEFAULT_CHARSET ='UTF-8'
#Directory Structure
MODELS_DIR = os.path.abspath('Models')
VIEWS_DIR = os.path.abspath('Views')
CONTROLLERS_DIR = os.path.abspath('Controllers')

BASE_VIEWS_DIR = os.path.join(VIEWS_DIR, 'bases')
BLOCK_VIEWS_DIR = os.path.join(VIEWS_DIR, 'blocks')
PAGE_VIEWS_DIR = os.path.join(VIEWS_DIR, 'pages')
FORM_VIEWS_DIR = os.path.join(VIEWS_DIR, 'forms')
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
