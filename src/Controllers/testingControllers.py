#from django.template import context, Template
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
from lib.halicea import ContentTypes as ct
from lib.halicea import xml2obj
class testingController(hrh):
    @ClearDefaults()
    @Default(method='gen')
    @Handler(method='view_xml', operation='xml')
    def SetOperations(self):pass
    
    @ResponseHeaders(**{'Content-Type':ct.XML})
    @View(**{'templateName':'results.xml'})
    def view_xml(self, *args, **kwargs):
        return {}

    @View(**{'templateName':'testingController_gen.html'})
    def gen(self, *args, **kwargs):
        p  = self.GetTemplatePath(templateName='results.xml')
        obj = xml2obj.xml2obj(open(p, 'r').read())
        return {'obj':obj}