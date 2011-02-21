import pprint
from sys import stdout,stdin
from string import Template
from os import makedirs
from os.path import basename, dirname, join as pjoin, exists
#------------
from halicea.consoleHelpers import ask
from halicea.config import proj_settings as settings, MvcTemplateDirs
from halicea import config, packager
from halicea.baseClasses import Model, Property, Block
from halicea import locators, mvcPaths
from halicea.codeBlocksHelpers import HalCodeBlockLocator, InPythonBlockLocator
cblPy = InPythonBlockLocator()
cblHal = HalCodeBlockLocator()

libDir = 'lib'

inherits_from = 'db.Model'
def render(templatePath, context={}):
    str = open(templatePath, 'r').read()
    t = config.TEMPLATE_RENDERER(str)
    contextDict ={}
    contextDict.update(context)
    contextDict.update(config.djangoVars)
    contextDict.update(config.mvcPaths)
    contextDict.update(config.sufixesDict)
    return t.render(contextDict)

def setProperties(p, model):
    t = p.split(' ')
    if len(t)>1:
        prop = Property()
        prop.Name = t[0]
        prop.Options = []
        if config.types.has_key(t[1]): 
            prop.Type = config.types[t[1]]
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
        elif t[1]=='selfref':
            has_coll_name = reduce(lambda x,y: x==True or 
                                   (x is str and 'collection_name' in x) or 
                                    'collection_name' in y,
                                   t[propStart])
            if not has_coll_name:
                prop.Options.append('collection_name=\''+prop.Name.lower()+'_'+model.Name.lower()+'s\'')
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
            pprint.pprint(config.types)
        return False
operations = [x[0] for x in settings.DEFAULT_OPERATIONS.iteritems() 
              if x[1].has_key('view') and x[1]['view']]

def renderController(model=None , outStream=stdout, magicType='magic0', *args):
    MvcTemplateDirs= mvcPaths.getTemplatesDirs(magicType)
    MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
    m = model
    #set operation templates
    methodTemplates = []
    for k, v in settings.DEFAULT_OPERATIONS.iteritems():
        if isinstance(v['method'], str):
            methodTemplates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],v['method']+'.txt'))
        else:
            methodTemplates.append(pjoin(MvcTemplateDirs['OPRTMPL_DIR'],v['method'].__name__+'.txt'))
    methodTemplates = list(set(methodTemplates))

    methods = map(lambda x: render(x, {'m':m}), methodTemplates)
    cntBl = None
    controllerFile = locators.LocateControllerModule(model.Package)
    if not exists(dirname(controllerFile)):
        makedirs(dirname(controllerFile))
    if not exists(controllerFile):
        cntBl =Block.loadFromFile(MvcTemplateFiles['CBTPath'], cblPy, render, {'m':m})
    else:
        cntBl =Block.loadFromFile(controllerFile, cblPy)
    classImport = Template('from ${modelsPath}.${modelModule} import ${modelClass}')\
        .substitute(modelsPath=basename(settings.MODELS_DIR),
                    modelModule=m.Package+settings.MODEL_MODULE_SUFIX,
                    modelClass=m.Name)
    if 'f' in args[0]:
        formImport = Template('from ${formsPath}.${formModule} import ${formClass}')\
            .substitute(formsPath=basename(settings.FORM_MODELS_DIR),
                    formModule=m.Package+settings.MODEL_FORM_MODULE_SUFIX,
                    formClass=m.Name+settings.MODEL_FORM_CLASS_SUFIX)
    if 'f' in args[0]:
        if not cntBl['imports']:
            imp = cntBl.createEmptyBlock('imports', cbl=cblPy)
            cntBl.insert(0, imp)
        cntBl['imports'].appendLines([formImport])
    cntBl['imports'].appendLines([classImport])
    
    cntBl.appendText(render(MvcTemplateFiles['CTPath'], {'m':m, 'methods':methods}))
    cntBl.saveToFile(controllerFile)

def renderControllerMethod(model=None, outputStream=stdout, magicType='magic0', *args):
    pass

def renderHandlerMap(model=None, outStream=stdout, magicType='magic0', *args):
    handlerMap = Block.loadFromFile(settings.HANDLER_MAP_FILE, cblPy)
    appControllers = handlerMap['ApplicationControllers']
    imports = handlerMap['imports']
    m = model
    #Create the block if it does not exists
    blockName = m.Package+settings.CONTROLLER_MODULE_SUFIX
    if not appControllers[blockName]:
        appControllers.createEmptyBlocks(blockName, cblPy)

    myBlock = appControllers[blockName]
    
    templ = Template("""('/${model}', ${controller}),""")
    urlEntry =templ.substitute(model=locators.BasePathFromName(m.FullName, '/'),
                               controller=m.Package+settings.CONTROLLER_MODULE_SUFIX+'.'+m.Name+settings.CONTROLLER_CLASS_SUFIX
                               )
    myBlock.append(Block.createLineBlock(urlEntry))

    importsLine= 'from '+basename(settings.CONTROLLERS_DIR)+' import '+m.Package+settings.CONTROLLER_MODULE_SUFIX
    if not imports[importsLine]:
        imports.append(Block.createLineBlock(importsLine))
    handlerMap.saveToFile(settings.HANDLER_MAP_FILE)

def renderModel(model=None, baseBlock=None, outputStream=stdout, magicType='magic0', *args):
    MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
    baseBlock.appendText(render(MvcTemplateFiles['MTPath'], {'m':model}))
    outputStream.write(str(baseBlock))

def renderModelForm(model=None, outputStream=stdout,magicType='magic0',*args):
    MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
    modelFormFile = locators.LocateFormModelModule(model.Package)
    if not exists(dirname(modelFormFile)):
        packager.createPackages(dirname(modelFormFile))
    frmBl = None
    if not exists(modelFormFile):
        frmBl = Block.loadFromFile(MvcTemplateFiles['FBTPath'], cblPy, render,{'m':model})
    else:
        frmBl = Block.loadFromFile(modelFormFile, cblPy)
    frmBl.appendText(render(MvcTemplateFiles['FTPath'], {'m':model}))
    outputStream.write(str(frmBl))

def renderPageView(model=None, outputStream=stdout, magicType='magic0', *args):
    MvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
    MvcTemplateDirs = mvcPaths.getTemplatesDirs(magicType)
    viewFolder = locators.LocatePagesDir(model.Package)
    if not exists(viewFolder): makedirs(viewFolder)

    for k in operations:
        Block\
            .loadFromFile(MvcTemplateFiles['VTPath'],cblHal, render, {'m':model,'formTemplate': model.Name+'Form_'+k })\
            .saveToFile(pjoin(viewFolder, model.Name+'_'+k+'.html'))

    #Forms Setup
    if magicType == 'magic0':
        formsFolder = locators.LocateFormsDir(model.Package)
        if not exists(formsFolder): makedirs(formsFolder)
        for k in operations:
            Block\
                .loadFromFile(pjoin(MvcTemplateDirs['FRMTMPL_DIR'], 'FormTemplate_'+k+'.txt'), cblHal, render, {'m':model, 'op':k})\
                .saveToFile(pjoin(formsFolder, model.Name+'Form_'+k+'.html'))

def renderFormView(model=None, outputStream=stdout, magicType='magic0', *args):
    pass

def makeMvc(args):
    
    arg = args[0]
    package = ''
    name =''
    magicLevel = settings.MagicLevel
    #TODO: set the MagicLevel
    #TODO: make try catch and display proper output if wrong sintax is entered
    if len(args)>1:
        name = args[1][args[1].rindex('.')+1:]
        package = args[1][:args[1].rindex('.')] 
    if len(args)>2:
        magicLevel = int(args[2])
    magicType = 'magic'+str(magicLevel)
    
    mvcTemplateFiles = mvcPaths.getTemplateFiles(magicType)
    mvcTemplateDirs = mvcPaths.getTemplatesDirs(magicType)
    m = Model()
    #TODO: Validation needs to be added here
    if not (name and package):
        m.Package = ask('PackageName: ', '*')
        m.Name = ask('ModelName: ', '*')
    else:
        m.Package = package
        m.Name = name

    if 'm' in arg:
        #TODO: set to according to an argument
        m.InheritsFrom = inherits_from
        i = 0
        print '.'*14+'class '+m.FullName+'('+m.InheritsFrom+'):'
        p = True #Do-While
        while p:
            p = raw_input('Property'+str(i)+'>'+'.'*(9-len(str(i))))
            if setProperties(p, m): i+=1
    else:
        #Create a Model instance out of specific class if exists
        raise NotImplemented('This feature is not implemented yet')

    if ask('Save?'):
        if 'm' in arg:
            #Model setup
            modelFile = locators.LocateModelModule(m.Package)
            baseBlock = Block.openOrCreate(modelFile, cblPy, render, {'m':m}, open(mvcTemplateFiles['MBTPath'], 'r').readlines())
            stream = open(modelFile, 'w')
            renderModel(m, baseBlock, stream, magicType=magicType)
            stream.close()
            #End Model Setup
        if 'f' in arg:
            #ModelForm Setup
            mfPath = locators.LocateFormModelModule(m.Package)
            baseBlock = Block.openOrCreate(mfPath, cblPy, render, {'m':m}, open(mvcTemplateFiles['FBTPath'], 'r').readlines())
            stream = open(mfPath, 'w')
            renderModelForm(m, baseBlock,stream,magicType)
            stream.close()
            #End ModelForm Setup
        if 'v' in arg:
            viewFolder = locators.LocatePagesDir(m.Package)
            #if we only want an empty view
            if not m:
                pass
            #if we want to generate the view by the model provided
            else:
                #if we dont want to use magic but to generate the default code instead
                if not magicLevel:
                    for k in operations:
                        baseBlock  = Block.openOrCreate(pjoin(viewFolder, m.Name+'_'+k+'.html'), cblHal, render, {'m':m,'formTemplate': m.Name+'Form_'+k }, open(mvcTemplateFiles['VTPath'],'r').readlines())
                        baseBlock.saveToFile(pjoin(viewFolder, m.Name+'_'+k+'.html'))
                        Block\
                            .loadFromFile(mvcTemplateFiles['VTPath'],cblHal, render, {'m':m,'formTemplate': m.Name+'Form_'+k })\
                            .saveToFile(pjoin(viewFolder, m.Name+'_'+k+'.html'))
                else: #here the magic will be used and we dont need some special view
                    pass
                renderPageView(model=m, magicType=magicType)
        if 'c' in arg:
            #Controller Setup
            controllerFile = open(locators.LocateControllerModule(m.Package), 'w')
            renderController(m, controllerFile, magicType, arg)
            controllerFile.close()
            #End Controller Setup
        if 'h' in arg:
            #HandlerMap Setup
            handlerMapFile = open(config.proj_settings.HANDLER_MAP_FILE, 'w')
            renderHandlerMap(m, handlerMapFile, magicLevel)
            handlerMapFile.close()
            #End HandlerMap

    m=None

def delMvc(mvc, modelFullName):
    pass