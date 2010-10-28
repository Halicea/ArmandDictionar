import os
import sys
from os.path import join as pjoin
from os.path import abspath, dirname
APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
if os.name == 'nt':
    #APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
    APPENGINE_PATH = 'C:\\devApps\\google_appengine'
PROJ_LOC = pjoin(dirname(__file__), '../src')
sys.path.append(abspath(pjoin(PROJ_LOC)))

#urlTemplate = '/$Package/$Model/$Action'
urlTemplate = '/$Package/$Model/?op=$Action'
import settings as proj_settings