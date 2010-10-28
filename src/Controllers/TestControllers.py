import settings
from lib.HalRequestHandler import HalRequestHandler as hrh
from lib.decorators import *
from google.appengine.ext import db
##################################################
from Models.TestModels import Mdl, MdlForm 
class MdlController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def insert(self):
        instance = None
        if self.params.key:
            instance = Mdl.get(self.params.key)
        form=MdlForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Mdl is saved'
            self.redirect(MdlController.get_url())
        else:
            self.SetTemplate(templateName = 'Mdl_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'MdlForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Mdl.get(self.params.key)
            if item:
                item.delete()
                self.status ='Mdl is deleted!'
            else:
                self.status='Mdl does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(MdlController.get_url())

    def list(self):
        self.SetTemplate(templateName='Mdl_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'MdlList': Mdl.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)

    def show(self):
        self.SetTemplate(templateName='Mdl_shw.html')
        if self.params.key:
            item = Mdl.get(self.params.key)
            if item:
                result = {'op':'upd', 'MdlForm': MdlForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Mdl does not exists'
                self.redirect(MdlController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'MdlForm':MdlForm()})
