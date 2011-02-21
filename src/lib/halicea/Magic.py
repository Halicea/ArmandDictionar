import settings
import os
class MagicSet(object):
    @staticmethod
    def getControllerClass(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        name = moduleBase+settings.CONTROLLER_MODULE_SUFIX+'.'+nameBase+settings.CONTROLLER_CLASS_SUFIX
        result = None
        exec('result = Controllers.'+name)
        return result
    @staticmethod
    def getModelClass(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        nameBase = nameBase+settings.MODEL_FORM_CLASS_SUFIX
        #Do Caching inhere instead of reloading it all te time
        result = None
        exec('from '+os.path.basename(settings.FORM_MODELS_DIR)+'.'+moduleBase+' import '+nameBase)
        exec('result ='+nameBase)
        return result
    @staticmethod
    def getViewDir(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        nameBase = nameBase+settings.MODEL_FORM_CLASS_SUFIX
        #Do Caching inhere instead of reloading it all te time
        result =None
        exec('from '+os.path.basename(settings.FORM_MODELS_DIR)+'.'+moduleBase+' import '+nameBase)
        exec('result ='+nameBase)
        return result
    @staticmethod
    def getFormClass(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        moduleBase = moduleBase+settings.MODEL_FORM_MODULE_SUFIX
        nameBase = nameBase+settings.MODEL_FORM_CLASS_SUFIX
        #Do Caching inhere instead of reloading it all te time
        result =None
        try:
            importStmt = 'from '+os.path.basename(settings.FORM_MODELS_DIR)+'.'+moduleBase+' import '+nameBase
            exec(importStmt)
            exec('result ='+nameBase)
        except Exception, ex:
            raise ex 
        return result
    @staticmethod
    def baseName(mvcItemInstance, splitParts = False):
        modPart = mvcItemInstance.__class__.__module__
        clsPart = mvcItemInstance.__class__.__name__

        for t in [settings.CONTROLLER_MODULE_SUFIX,
                  settings.MODEL_MODULE_SUFIX,
                  settings.MODEL_FORM_MODULE_SUFIX]:
            if t and modPart.endswith(t):
                modPart = modPart[:-len(t)]
                break;
        for t in [settings.CONTROLLER_CLASS_SUFIX,
                  settings.MODEL_CLASS_SUFIX,
                  settings.MODEL_FORM_CLASS_SUFIX]:
            if t and clsPart.endswith(t):
                clsPart = clsPart[:-len(t)]
                break;
        if splitParts:
            return modPart[modPart.index('.')+1:], clsPart
        else:
            return modPart[modPart.index('.')+1:]+'.'+clsPart