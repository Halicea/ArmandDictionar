#{%block imports%}
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
from Forms.ArmanListingForms import ArmanForm, AddressForm
from Models.ArmanListingModels import Arman, Address
from Controllers import BaseControllers
from django.utils import simplejson
#{%endblock%}
class Connection(object):
    def __init__(self, arman):
        self.Arman = arman
        self.AddedBy = arman.AddedBy.mapped_to_arman.get()

class ArmansBaseController(hrh):
    def render_dict(self, basedict):
        res = super(ArmansBaseController, self).__render_dict(basedict)
        arman = self.User.mapped_to_arman.get()
        connList =[]
        if arman:
            connList = arman.RelatedArmans
            res.update({'arman':arman})
        res.update({'connectionsList':[Connection(arman) for arman in connList]})
        return res

class ArmanSearchController(ArmansBaseController):
    @Default(method='search')
    def SetOperations(self):pass

    def search(self, *args):
        if self.isAjax:
            self.SetTemplate("form", "ArmanListing", "ArmanForm_index.html")
        else:
            self.SetTemplate(templateName = "Arman_index.html")
        ArmanList = Arman.search(name=self.params.name, surname=self.params.surname, 
                            armanSurname=self.params.armanSurname, 
                            city=self.params.city, street=self.params.street, limit=10, offset= self.params.offset or 0)
        return {"ArmanList":ArmanList}

class ArmanController(ArmansBaseController):
    @ClearDefaults()
    @Default('edit')
    @Handler(method='edit', operation='edit')
    @Handler(method='delete', operation='delete')
    @Handler(method='index', operation='index')
    def SetOperations(self):pass
    @LogInRequired()
    def delete(self, *args):
        if self.params.key:
            Arman.get(self.params.key).delete()
            self.redirect(self.get_url())
        else:
            self.status = "Not Allowed"
    @LogInRequired()
    @View(**{'templateName':"Arman.html"})
    def edit(self, *args):
        if self.request.method == 'GET':
            if self.params.key: #edit
                instance = Arman.get(self.params.key)
                if not instance:
                    self.status = 'Not Valid Arman'
                    self.respond()
                    return
                else:
                    return {'op':'edit',
                            'ArmanForm': ArmanForm(instance=instance),
                            'register':False}
            else: #new
                form = ArmanForm()
                instance = self.User.mapped_to_arman.get()
                if not instance:
                    form.MappedToCurrent = True
                result= {'op':'save',\
                        'register':True,\
                        'ArmanForm':form,\
                       }
                return result
        else:
            instance = None
            if self.params.key:
                instance = Arman.get(self.params.key)
            form = ArmanForm(data = self.request.POST, instance=instance)
            if form.is_valid():
                mappedTo = None
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
    @ClearDefaults()
    @Default('getAddress')
    def SetOperations(self):pass
    
    @Post()
    def getAddress(self, *args, **kwargs):
        if self.params.key:
            arman = Arman.get(self.params.key)
            addressForm = AddressForm(instance=arman.PersonalAddress)
            return addressForm.as_table()
