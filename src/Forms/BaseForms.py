from django.forms import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from Models.BaseModels import *

class PersonForm(ModelForm):
    class Meta():
        model = Person
class RoleForm(ModelForm):
    class Meta():
        model=Role
class RoleAssociationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleAssociationForm, self).__init__(*args, **kwargs)
        self.fields['Person'].queryset = Person.all().fetch(limit=100)
    class Meta():
        model=RoleAssociation
##End Invitation
from django.forms import Form
class InvitationForm(Form):
    Email = fields.EmailField(required=True)