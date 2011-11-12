#!/usr/bin/env python
import sys, subprocess, webbrowser, os
from os.path import join as pjoin
from string import Template
#-----------------
from halicea.config import installPath
from halicea.consoleHelpers import extractAgrs
from halicea.ioUtils import saveTextToFile, getTextFromPath
from halicea.mvcManager import makeMvc, delMvc
from halicea.projectManager import newProject
from halicea.codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
from halicea.templateHelpers import convertToReal, convertToTemplate
from halicea import config, packager
cblPy = InPythonBlockLocator()
cblHal = HalCodeBlockLocator()
if os.name!='nt':
    import readline

def tail(arr, cnt):
    if len(arr)<cnt: 
        return []
    else: 
        return arr[-cnt:]
#AutoCompletion
values =['project', 'mvc','vc','mc', 'mv','m','v','c','run','deploy']
modelsStructure ={}
commandsDict={'*':{ 'new':{'template':{}, 'real':{}}, 'project':{}, 
                    'mvcfh':{},
                    'del':{'package':{}, 'model':{}}, 
                    'deploy':{'--no_cookies':{},'--email=':{}}, 
                    'run':{'--port=':{}, '--clear_datastore=':{}, '--datastore_path=':{}},
                    'pack':{'package':{}},
                    'unpack':{'package':{}},
                    'git':{'log':{},'init':{}, 'push':{'origin':{'master':{}}}, 'commit':{'-a':{}, '-am \"':{}}, 'add':{'.':{}} },
                    'deploy':{},
                    'exit':{}
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
#        else:
#            print 'Not a valid command'
        #return
    if True: #TODO: Change to else:
        if set(args[0]).issubset(set('mvfch')):
            makeMvc(args)
        elif args[0]=='del' and len(args)>=2:
            if args[1]=='package':
                pname = ''
                if len(args)==2:
                    pname = raw_input('Enter Package Name: ')
                else:
                    pname=args[2]
                packager.delete(pname)
            elif set(args[1]).issubset(set('mvc')):
                cname = ''
                pname = ''
                if len(args)==2:
                    cname=raw_input('EnterTheModelClass: ')
                else:
                    cname=args[2]
                delMvc(args[1], cname)
        elif args[0]=='run':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:])
            command = Template('python $appserver $proj $options').substitute(
                                    appserver = pjoin(config.APPENGINE_PATH, 'dev_appserver.py'),
                                    proj=config.PROJ_LOC,
                                    options = options)
            # print command
            subprocess.Popen(command, shell=True, stdout=sys.stdout, stdin=sys.stdin)
            webbrowser.open('http://localhost:8080')
        elif args[0]=='pack' and len(args)>3:
            if args[1]=='package':
                packager.pack(args[2], args[3])
        elif args[0]=='unpack' and len(args)>=3:
            if args[1]=='package':
                packager.unpack(args[2], args[3])
        elif args[0]=='deploy':
            options = ''
            if len(args)>1:
                options = ' '.join(args[1:])
            command = Template('python $appcfg update $options $proj').substitute(
                                  appcfg = pjoin(config.APPENGINE_PATH, 'appcfg.py'),
                                  proj = config.PROJ_LOC,
                                  options = options)
            subprocess.Popen(command, Shell=True)
        elif args[0]=='console':
            pass
        elif args[0]=='git':
            fi,fo,fe= os.popen3(' '.join(args))
            for ln in fo.readlines():
                print 'git:', ln.replace('\n', '')
            for i in fe.readlines():
                print "error:",i.replace('\n', '')
#           for i in fi.readlines():
#                print "input->",i, ':'
        else:
            print 'Not Valid Command [mvc, run, console]'
        return
if __name__ == '__main__':
    sysargs = sys.argv
    try:
        if len(sysargs)>1:
            main(sysargs[1:])
        else:
            'Halicea Command Console is Opened'
            while True:
                args =raw_input('hal>').split()
                if not(len(args)==1 and args[0]=='exit'):
                    main(args)
                else:
                    print 'Halicea Command Console exited'
                    break;
    except KeyboardInterrupt:
        print 'Halicea Command Console exited'
