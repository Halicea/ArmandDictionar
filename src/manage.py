                                    #!/usr/bin/env python
import sys
import os
import shutil
import settings
import pprint
from os.path import join as pjoin
from os.path import abspath
from os.path import dirname
from os.path import basename
if os.name!='nt':
    import readline

#Template Configuration
installPath = dirname(abspath(__file__))
TMPL_DIR = 'Templates'
FRMTMPL = pjoin(TMPL_DIR, 'FormTemplates')
OPRTMPL = pjoin(TMPL_DIR, 'OperationTemplates')

MTPath = pjoin(TMPL_DIR, 'ModelTemplate.txt')
VTPath = pjoin(TMPL_DIR, 'ViewTemplate.txt')
CTPath = pjoin(TMPL_DIR, 'ControllerTemplate.txt')

#Set django in pythonpath
sys.path.append(settings.APPENGINE_PATH)
sys.path.append(pjoin(settings.APPENGINE_PATH, 'lib', 'django' ))
sys.path.append(pjoin(settings.APPENGINE_PATH, 'lib', 'webob' ))
sys.path.append(pjoin(settings.APPENGINE_PATH, 'lib', 'yaml','lib' ))
###
os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
from django import template

types ={'txt':'db.TextProperty',
        'str':'db.StringProperty',
        'bln':'db.BooleanProperty',
        'dtm':'db.DateTimeProperty',
        'date':'db.DateProperty',
        'email':'db.EmailProperty',
        'int':'db.IntegerProperty',
        'float':'db.FloatProperty',
        'ref':'db.ReferenceProperty'}

djangoVars = {'ob':'{{', 'cb':'}}', 'os':'{%', 'cs':'%}', }

mvcPaths = {"modelsPath":basename(settings.MODELS_DIR), 
            'viewsPath':basename(settings.VIEWS_DIR), 
            'controlersPath':basename(settings.CONTROLLERS_DIR)}
libDir = 'lib'
inherits_from = 'db.Model'

class Model(object):
    Package = ''
    Name = ''
    References = []
    Properties = []
    InheritsFrom = ''

class Property(object):
    Name = ''
    Type = ''
    Options = None
    Required = 'False'
    Default = None

def copy_directory(source, target, ignoreDirs=[], ignoreFiles=[]):
    ignoreDirsSet =set(ignoreDirs)
    ignoreFilesSet =set(ignoreFiles) 
    if not os.path.exists(target):
        os.mkdir(target)
    for root, dirs, files in os.walk(source): 
        ignoreCurrentDirs = list(ignoreDirsSet.intersection(set(dirs)))
        
        for t in ignoreCurrentDirs:
            print 'Ignoring', t
            dirs.remove(t)  # don't visit .svn directories           
        for file in files:
            if os.path.splitext(file)[-1] in ignoreFiles:
                print 'skipped', file
                continue
            from_ = os.path.join(root, file)           
            to_ = from_.replace(source, target, 1)
            to_directory = os.path.split(to_)[0]
            if not os.path.exists(to_directory):
                os.makedirs(to_directory)
            shutil.copyfile(from_, to_)
def appendInBlocks(filePath, blockValuesDict):
    curBlockName = ''
    f = open(filePath, 'r'); 
    lines=f.readlines(); 
    f.close()
    newlines = []
    curBlockName = ''
    for line in lines:
        if '{%block' in line.strip() or '{% block' in line:
            mline = line.strip(); mline = mline.replace('{% block', '{%block')
            fromIndex=mline.index('{%block')+len('{%block')
            toIndex = fromIndex+mline[fromIndex:].index('%}')
            curBlockName = mline[fromIndex:toIndex].strip()
#           Append the lines if in the same block
        if '{%endblock%}' in line.replace(' ',''):
            if blockValuesDict.has_key(curBlockName):
                for nline in blockValuesDict[curBlockName]:
                    newlines.append(nline+'\n')
            curBlockName = ''
        newlines.append(line)
    f = open(filePath, 'w')
    f.writelines(newlines)
    f.close()

def importModel(package, name):
    sys.path.append(settings.MODELS_DIR)
    exec 'import '+basename(settings.MODELS_DIR)
    moduleName =  basename(settings.MODELS_DIR)+'.'+package+'.'+name
    print moduleName
    mod = __import__(moduleName)
    components = name.split('.')
    for comp in components:
        mod = getattr(mod, comp)
    return mod

def makeMvc(arg):
    operations = [x[0] for x in settings.DEFAULT_OPERATIONS.iteritems() 
                  if x[1].has_key('view') and x[1]['view']]
    templates = [os.path.join(OPRTMPL,settings.DEFAULT_OPERATIONS[x]['method']+'.txt')
                 for x in settings.DEFAULT_OPERATIONS.iterkeys()]
    templates = list(set(templates))

    m = Model()
    #TODO: Validation needs to be added here
    m.Package = raw_input('PackageName: ')
    m.Name = raw_input('ModelName: ')
    if 'm' in arg:
        m.InheritsFrom = inherits_from
        print 'Enter Property(Press Enter for End)'
        print 'Format', '[Name] [Type] <param1=value param1=value ...>'
        print 'Types', str([k for k in types.iterkeys()])
        i = 0
        print '.'*14+'class '+m.Name+'('+m.InheritsFrom+'):'
        p = True #Do-While
        while p:
            p = raw_input('Property'+str(i)+'>'+'.'*(9-len(str(i))))
            if setProperties(p, m):
                i+=1
        print render(m, MTPath)
        print "*"*20
    else:
        m = importModel(m.Package, m.Name)
        print m.parameters
    
    if 'v' in arg:
        print render(m, VTPath, {'operations':templates})
        print "*"*20
    
    if 'c' in arg:
        methods = map(lambda x: render(m, x), templates)
        print render(m, CTPath, {'methods':methods})
    
    save = raw_input('Save(y/n)>')
    if save.lower()=='y':
        if 'm' in arg:
            # Model setup
            modelFile = pjoin(settings.MODELS_DIR, m.Package+settings.MODEL_MODULE_SUFIX+'.py')
            if not os.path.exists(modelFile):
                f = open(modelFile, 'w')
                f.write('import settings\n')
                f.write('from google.appengine.ext.db.djangoforms import ModelForm\n')
                f.write('from google.appengine.ext import db\n')
                f.write('#'*50+'\n')
                f.close()
            f= open(modelFile, 'a')
            f.write(render(m, MTPath))
            f.close()
            # End Model Setup
        if 'v' in arg:
            #View Setup
            viewFolder = pjoin(settings.PAGE_VIEWS_DIR, m.Package)
            if not os.path.exists(viewFolder): os.makedirs(viewFolder)
            for k in operations:  
                f = open(pjoin(viewFolder, m.Name+'_'+k+'.html'), 'w')
                f.write(render(m, VTPath, {'formTemplate': m.Name+'Form_'+k }))
                f.close()
            #End Views Setup
            #Forms Setup
            formsFolder = pjoin(settings.FORM_VIEWS_DIR, m.Package)
            if not os.path.exists(formsFolder): os.makedirs(formsFolder)
            for k in operations:
                f = open(pjoin(formsFolder, m.Name+'Form_'+k+'.html'), 'w')
                # print k, 
                f.write(render(m, os.path.join(FRMTMPL, 'FormTemplate_'+k+'.txt'),{'op':k }))
                f.close()
            #End Form Setup
        if 'c' in arg:
            #Controller Setup
            controllerFile = pjoin(settings.CONTROLLERS_DIR, m.Package+settings.CONTROLLER_MODULE_SUFIX+'.py')
            if not os.path.exists(controllerFile):
                f = open(controllerFile, 'w')
                f.write('import settings\n')
                f.write('from lib.HalRequestHandler import HalRequestHandler as hrh\n')
                f.write('from lib.decorators import *\n')
                f.write('from google.appengine.ext import db\n')
                f.write('#'*50+"\n")
                f.close()
            f= open(controllerFile, 'a')
            f.write(render(m, CTPath, {'methods':methods}))
            f.close()
            #End Controller Setup
            #Edit HandlerMap
            f = open(settings.HANDLER_MAP_FILE, 'r'); 
            blocks={'ApplicationControllers':
                           ['(\'/'+m.Package.replace('.','/')+'/'+m.Name+'\', '+m.Package+settings.CONTROLLER_MODULE_SUFIX+'.'+m.Name+'Controller),',],
                    'imports':
                        ['from '+basename(settings.CONTROLLERS_DIR)+' import '+m.Package+settings.CONTROLLER_MODULE_SUFIX,]
                   }
            appendInBlocks(settings.HANDLER_MAP_FILE, blocks)
    m=None

def render(model, templatePath, additionalVars={}):
    
    str = open(templatePath, 'r').read() 
    t = template.Template(str)
    dict = {'m':model}
    dict.update(djangoVars)
    dict.update(mvcPaths)
    dict.update(additionalVars)
    context = template.Context(dict)
    return t.render(context)

def setProperties(p, model):
    t = p.split(' ')
    if len(t)>1:
        prop = Property()
        prop.Name = t[0]
        prop.Options = []
        if types.has_key(t[1]): 
            prop.Type = types[t[1]]
        else:
            print 'Not valid property type'
            return False
        propStart = 2
        if t[1]=='ref':
            prop.Options.insert(0, t[propStart])
            has_coll_name = reduce(lambda x,y: x==True or 
                                   (x is str and 'collection_name' in x) or 
                                    'collection_name' in y,
                                   t[propStart])
            if not has_coll_name:
                prop.Options.append('collection_name=\''+prop.Name.lower()+'_'+model.Name.lower()+'s\'')
            propStart+=1
        if len(t)>propStart:
            for op in t[propStart:]:
                if '=' in op:
                    prop.Options.append(op)
                else:
                    print 'Not valid Option %s'%op
                    return False
#        print model.Properties
        model.Properties.append(prop)
        return True
    else:
        if len(t)==1 and  t[0]:
            print 'Must provide Type:'
            pprint.pprint(types)
        return False
def newProject(toPath):
    doCopy = True
    if os.path.exists(toPath):
        overwrite = raw_input('Path Already Exists!, Do you want to overwrite?(y/n):')
        if overwrite == 'y':
            shutil.rmtree(toPath)#os.makedirs(toPath)
        else:
            doCopy = False
    if doCopy:
        # print fromPath,'=>', toPath
        # raw_input()
        copy_directory(installPath, toPath, ['.git',], ['.gitignore','.pyc',])
        str = open(pjoin(toPath, 'app.yaml'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath).lower())
        str = str.replace('{{handler}}', settings.HANDLER_MAP_FILE)
        f = open(os.path.join(toPath, 'app.yaml'), 'w')
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
        
        os.rename(pjoin(toPath,'halicea.py'), pjoin(toPath,'manage.py'))
        os.remove(pjoin(toPath, '.InRoot'))
        print 'Project is Created!'

def convertToTemplate(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    for k, v in input.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    result = result.replace('{-{','{{')
    result = result.replace('}-}','}}')
    return result

def convertToReal(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(k, v)
    for k, v in input.iteritems():
        result=result.replace(k, v)
    return result

def getTextFromPath(filePath):
    templ = ''
    if filePath[-1]==']' and filePath.rindex('[')>0:
        fn= filePath
        lindex = int(fn[fn.rindex('[')+1:fn.rindex(':')])
        rindex = int(fn[fn.rindex(':')+1:-1])
        f = open(filePath[:filePath.rindex('[')], 'r')
        templ = ''.join(f.readlines()[lindex:rindex])
        f.close()
    else:
        templ = open(filePath,'r').read()
    return templ
def extractAgrs(paramsList):
    return dict(map(lambda x:(x[:x.index('=')], x[x.index('=')+1:]), paramsList))
def saveTextToFile(txt, skipAsk=False, skipOverwrite=False):
    save = skipAsk and raw_input('Save to File?(y/n):')
    if save=='y':
        filePath = raw_input('Enter the Path>')
        if os.path.exists(filePath):
            again = True
            while again:
                again = False
                p = skipOverwrite and raw_input('File already Exists, (o)verwrite, (a)ppend, (p)repend or (c)ancel?>')
                if p=='o' or p==False:
                    f = open(filePath, 'w'); f.write(txt); f.close()
                elif p=='a':
                    f = open(filePath, 'a'); f.write(txt); f.close()
                elif p=='p':
                    f = open(filePath, 'r'); txt = txt+'\n'+f.read(); f.close()
                    f = open(filePath, 'w'); f.write(txt); f.close()
                elif p == 'c':
                    pass
                else:
                    print 'Not Valid Command, Options: o, a, p, c lowercase only!'
                    again = True
                    
                if not again and p!='c':
                    print 'File saved at \"%s\"!'%filePath
        else:
            f = open(p, 'w'); f.write(txt); f.close()


values =['project', 'mvc','vc','mc', 'mv','m','v','c','run','deploy']
modelsStructure ={}
commandsDict={'*':{'new':{'template':{}, 'real':{}}, 'project':{}, 
                    'mvc':{}, 
                    'deploy':{'--no_cookies':{},'--email=':{}}, 
                    'run':{'--port=':{}}
                    }
                }
mvcStates = {'package':{},'class':{}, 'prop':{'ref':modelsStructure} }

completions={}
currentState = ''
def completer(text, state):
    line = readline.get_line_buffer()
    enterstate = line.split()
    enterstate.insert(0,'*')
    if line and not line[-1]==' ':
        searchText = enterstate.pop()
    else:
        searchText = ''
    finalDict = commandsDict
    try:
        for k in enterstate:
            finalDict = finalDict[k]
    except:
        finalDict = {}
    matches = [value for value in finalDict.iterkeys() if value.upper().startswith(searchText.upper())]
    try:
        return matches[state]
    except IndexError:
        return None

if os.name!='nt':
    readline.set_completer(completer)
    readline.parse_and_bind('tab: menu-complete')
baseusage = """
Usage haliceamvc.py [projectPath]
Options: [create]
"""
def main(args):
    # can do this in install on local mode    
    if args[0]=='new' and len(args)>2:
        if args[1]=='template':
            templ = getTextFromPath(args[2])
            input=len(args)>3 and extractAgrs(args[3:]) or {}
            txt = convertToTemplate(templ, input)
            print txt; print 
            saveTextToFile(txt)
            return
        elif args[1] =='real':
            templ = getTextFromPath(args[2])
            input=len(args)>3 and extractAgrs(args[3:]) or {}
            txt = convertToReal(templ, input)
            print txt; print
            saveTextToFile(txt)
            return
        else:
            print 'Not valid type for new'
            return
    isInInstall = os.path.exists(pjoin(installPath, '.InRoot'))
#    isInInstall=True
    if isInInstall:
        if args[0]=='project' and len(args)>1:
            newProject(args[1])
        else:
            print 'Not a valid command'
        return
    else:
        if set(args[0]).issubset(set('mvc')):
            makeMvc(args[0])
        elif args[0]=='run':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:]) 
            command = pjoin(settings.APPENGINE_PATH, 'dev_appserver.py')+' '+os.path.abspath(os.path.dirname(__file__)+' '+options)
            # print command
            os.system(command)
        elif args[0]=='deploy':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:]) 
            command = pjoin(settings.APPENGINE_PATH, 'appcfg.py')+' update '+options+' '+os.path.abspath(os.path.dirname(__file__))
            # print command
            os.system(command)
        elif args[0]=='console':
            pass
        else:
            print 'Not Valid Command [mvc, run, console]'
        return
if __name__ == '__main__':
    try:
        if len(sys.argv)>1:
            main(sys.argv[1:])
        else:
            'Halicea Command Console is Opened'
            while True:
                args =raw_input('hal>').split()
                if not(len(args)==1 and args[0]=='exit'):
                    main(args)
                else:
                    break;
    except KeyboardInterrupt:
        print 'Halicea Command Console exited'
