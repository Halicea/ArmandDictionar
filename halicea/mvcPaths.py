import config
def getTemplatesDirs(magicType):
    MvcTemplateDirs = {}; MvcTemplateDirs.update(config.MvcTemplateDirs)
    for k,v in MvcTemplateDirs.iteritems():
        MvcTemplateDirs[k]=v.replace('{{magicLevel}}', magicType)
    return MvcTemplateDirs
def getTemplateFiles(magicType):
    MvcTemplateFiles = {}; MvcTemplateFiles.update(config.MvcTemplateFiles)
    for k,v in MvcTemplateFiles.iteritems():
        MvcTemplateFiles[k]=v.replace('{{magicLevel}}', magicType)
    return MvcTemplateFiles
