#{%block imports%}
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import AdminOnly, LogInRequired, InRole
from Forms.ArmanListingForms import ArmanForm, AddressForm
from Models.ArmanListingModels import Arman
from Controllers import BaseControllers
#{%endblock%}

class ArmanController(hrh):
    def SetOperations(self):
        self.operations ={
                          'default':{'method':self.new},
                          'lst':{'method':self.index},
                          'save':{'method':self.save},
                          }
    def new(self, *args):
        instance = None
        if self.params.key:
            instance = Arman.get(self.params.key)
        return {'op':'save', 'ArmanForm':ArmanForm(instance=instance)}
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Arman.get(self.params.key)
        form = ArmanForm(data = self.request.POST,instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Arman saved'
            self.redirect(ArmanController.get_url())
        else:
            self.SetTemplate(templateName='Arman_shw.html')
            self.status = 'Error in Data'
            return  {'ArmanForm':form}
        
    def index(self, *args):
        return {'ArmanList':Arman.all().fetch(limit=100, offset=0)}
