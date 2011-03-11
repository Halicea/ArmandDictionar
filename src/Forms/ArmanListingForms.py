from lib.djangoFormImports import widgets, fields
from google.appengine.ext.db.djangoforms import ModelForm
#{%block imports%}
from Models.ArmanListingModels import Address, Arman
#{%endblock%}

from lib.ArmanDict import MunicipalityList
class AddressForm(ModelForm):
    Municipality = fields.Select(choices=MunicipalityList.MunicipalityList)
    class Meta():
        model = Address
class ArmanForm(ModelForm):
    PersonalAddressForm = AddressForm()
    class Meta():
        model = Arman 
        exclude = ('AddedBy', 'DateAdded')
    def save(self, commit=False):
        res = ModelForm.save(self, False)
        addr = self.PersonalAddressForm.save(commit=False)
        if commit:
            if self.is_valid():
                addr.put()
                res.PersonallAddress = addr
                res.put()
            else:
                raise NotImplementedError()
        return res, addr
    def __init__(self, data=None, instance=None):
        ModelForm.__init__(self, data=data, instance=instance)
        if instance:
            self.PersonalAddressForm = AddressForm(data=data, instance=instance.PersonalAddress)
        else:
            self.PersonalAddressForm = AddressForm(data=data)
    def is_valid(self):
        result = ModelForm.is_valid(self) 
        return self.PersonalAddressForm.is_valid() and result
