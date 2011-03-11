#{%block imports%}
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import AdminOnly, LogInRequired, InRole
from Forms.ArmanListingForms import ArmanForm, AddressForm
from Models.ArmanListingModels import Arman, Address
from Controllers import BaseControllers
#{%endblock%}

class ArmanController(hrh):
    def SetOperations(self):
        self.operations ={
                          'default':{'method':self.edit},
                          'edit':{'method':self.edit},
                          'index':{'method':self.index},
                          }
    def register(self,*args):
        pass
    @LogInRequired()
    def edit(self, *args):
        self.SetTemplate(templateName="Arman.html")
        if self.request.method == 'GET':
            instance = None
            relativeList=None
            op = self.params.op or 'save'
            if self.params.key:
                instance = Arman.get(self.params.key)
                if instance.PersonalAddress:
                    relativeList = instance.PersonalAddress.personal_adress_persons.fetch(limit=10)
            result= {'op':op,\
                    'register':True,\
                    'relativeList': relativeList,\
                    'ArmanForm':ArmanForm(instance=instance),\
                   }
            return result
        else:
            instance = None
            if self.params.key:
                instance = Arman.get(self.params.key)
            form = ArmanForm(data = self.request.POST,instance=instance)
            if form.is_valid():
                instance, address=form.save(commit=False)
                address.put()
                instance.PersonalAddress = address
                instance.put()
                relativeList = instance.PersonalAddress.personal_adress_persons.fetch(limit=10)
                self.status = 'Arman saved'
                self.login_user(instance.UserName, instance.Password)
                return {
                    'register':False,
                    'relativeList': relativeList,
                    'ArmanForm':ArmanForm(instance=instance),
                   }
            else:
                self.SetTemplate(templateName='Arman.html')
                self.status = 'Error in Data'
                return  {'ArmanForm':form}
    
    def index(self, *args):
        return {'ArmanList':Arman.all().fetch(limit=100, offset=0)}
