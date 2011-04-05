#{%block imports%}
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import AdminOnly, LogInRequired, InRole
from Forms.ArmanListingForms import ArmanForm, AddressForm
from Models.ArmanListingModels import Arman, Address
from Controllers import BaseControllers
from django.utils import simplejson
#{%endblock%}

class Connection(object):
    def __init__(self, arman):
        self.Arman = arman
        self.AddedBy = arman.AddedBy.mapped_to_arman.get()

class ArmanController(hrh):
    def SetOperations(self):
        self.operations ={
                          'default':{'method':self.edit},
                          'edit':{'method':self.edit},
                          'index':{'method':self.index},
                          }
    def registerself(self,*args):
        pass
    def editself(self,*args):
        pass
    def new(self, *args):
        pass
    
    @LogInRequired()
    def edit(self, *args):
        self.SetTemplate(templateName="Arman.html")
        if self.request.method == 'GET':
            if self.params.key: #edit
                instance = Arman.get(self.params.key)
                if not instance:
                    self.status = 'Not Valid Arman'
                    self.respond()
                    return
                else:
                    return {'connectionsList':[Connection(arman) for arman in instance.RelatedArmans],
                            'op':'edit',
                            'ArmanForm': ArmanForm(instance),
                            'register':False}
            else: #new
                form = ArmanForm()
                instance = self.User.mapped_to_arman.get()
                if not instance:
                    form.MappedToCurrent = True
                result= {'op':'save',\
                        'register':True,\
                        'connectionsList': instance and [Connection(arman) for arman in instance.RelatedArmans] or [],\
                        'ArmanForm':form,\
                       }
                return result
        else:
            instance = None
            if self.params.key:
                instance = Arman.get(self.params.key)
            form = ArmanForm(data = self.request.POST, instance=instance)
            if form.is_valid():
                if not self.params.key:
                    alreadyMapped = (self.User.mapped_to_arman.get() and [True] or [False])[0]
                    mappedTo = (alreadyMapped and [None] or [self.User])[0]
                instance=form.save(addedBy=self.User, mappedTo=mappedTo)
                self.status = 'Arman saved'
                return {
                    'connectionsList':[Connection(arman) for arman in instance.RelatedArmans],
                    'ArmanForm':ArmanForm(),
                   }
            else:
                self.SetTemplate(templateName='Arman.html')
                self.status = 'Error in Data'
                return  {'ArmanForm':form}
    @AdminOnly()
    def index(self, *args):
        return {'ArmanList':Arman.all().fetch(limit=100, offset=0)}
        
class AddressController(hrh):
    def SetOperations(self):
        self.operations = {'default':{'method':self.getAddress}}
    def getAddress(self, *args, **kwargs):
        if self.params.key:
            arman = Arman.get(self.params.key)
            addressForm = AddressForm(instance=arman.PersonalAddress)
            self.respond_static(addressForm.as_table())
