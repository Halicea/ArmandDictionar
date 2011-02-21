import os, shutil
from os.path import basename, join as pjoin, dirname, abspath
from halicea.ioUtils import copy_directory
from halicea.consoleHelpers import ask
from halicea.config import proj_settings as settings
installPath = dirname(dirname(abspath(__file__)))
def newProject(toPath):
    doCopy = True
    if os.path.exists(toPath):
        overwrite = ask('Path Already Exists!, Do you want to overwrite?')
        if overwrite:
            shutil.rmtree(toPath) #os.makedirs(toPath)
        else:
            doCopy = False
    if doCopy:
        copy_directory(installPath, toPath, ['.git',], ['.gitignore','.pyc','.InRoot',])
        str = open(pjoin(toPath,'src', 'app.yaml'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath).lower())
        str = str.replace('{{handler}}', basename(settings.HANDLER_MAP_FILE))
        f = open(os.path.join(toPath,'src', 'app.yaml'), 'w')
        f.write(str)
        f.close()

        str = open(pjoin(toPath, '.project'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath))
        f = open(os.path.join(toPath, '.project'), 'w')
        f.write(str)
        f.close()

        str = open(pjoin(toPath, '.pydevproject'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath))
        str = str.replace('{{appengine_path}}', settings.APPENGINE_PATH)
        f = open(pjoin(toPath, '.pydevproject'), 'w')
        f.write(str)
        f.close()

        if os.path.exists(pjoin(toPath, 'halicea.py')):
            os.rename(pjoin(toPath,'halicea.py'), pjoin(toPath,'manage.py'))

        print 'Project is Created!'
