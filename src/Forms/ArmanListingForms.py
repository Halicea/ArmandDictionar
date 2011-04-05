from lib.djangoFormImports import widgets, fields, BaseForm
#from django.forms import fields, widgets, forms
#from django.forms import BaseForm
from google.appengine.ext.db.djangoforms import ModelForm
#{%block imports%}
from Models.ArmanListingModels import Address, Arman
#{%endblock%}

from lib.ArmanDict import MunicipalityList
class AddressForm(ModelForm):
    Municipality = fields.ComboField(widget=widgets.Select(choices=MunicipalityList.MunicipalityList), required=True)
    class Meta():
        model = Address
class ArmanForm(ModelForm):
    PersonalAddressForm = AddressForm()
    MappedToCurrent = False
    class Meta():
        model = Arman
        exclude = ('AddedBy', 'DateAdded', 'PersonalAddress')
    def save(self, addedBy=None, mappedTo=None):
        addrInstance = None
#        if self.clean_data['PersonallAddressKey']:
#            addrInstance = Address.get(self.clean_data['PersonallAddressKey'])
        addr = self.PersonalAddressForm.save(commit=False)
        addr.put()
        if not self.instance:
            res = Arman.CreateNew(
                    mappedTo = mappedTo,
                    name = self.clean_data['Name'], 
                    surname = self.clean_data['Surname'], 
                    armansurname = self.clean_data['ArmanSurname'] or None, 
                    personalladress = addr,
                    email = self.clean_data['Email'] or None, 
                    facebook = self.clean_data['Facebook'] or None, 
                    mobilephone = self.clean_data['MobilePhone'] or None, 
                    homephone= self.clean_data['HomePhone'] or None, 
                    isspeakingarman = self.clean_data['IsSpeakingArman'], 
                    iswriteingarman = self.clean_data['IsWriteingArman'],
                    addedBy = addedBy,  
                    _isAutoInsert=True)
        else:
            res = ModelForm.save(self, commit=False)
        if self.is_valid():
            addr.put()
            res.PersonallAddress = addr
            res.put()
        else:
            raise NotImplementedError()
        return res
    def __init__(self, data=None, instance=None):
        ModelForm.__init__(self, data=data, instance=instance)
        if instance:
            self.PersonalAddressForm = AddressForm(data=data, instance=instance.PersonalAddress)
        else:
            self.PersonalAddressForm = AddressForm(data=data)
    def is_valid(self):
        result = ModelForm.is_valid(self) 
        return self.PersonalAddressForm.is_valid() and result


class SearchForm(BaseForm):
    Name = fields.Field(widget=widgets.TextInput)
    Surname = fields.Field(widget=widgets.TextInput)
    ArmanSurname = fields.Field(widget=widgets.TextInput)
    Municipality = fields.ComboField(widget=widgets.SelectMultiple(choices=MunicipalityList.MunicipalityList))
