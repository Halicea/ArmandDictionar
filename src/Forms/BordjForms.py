from lib.djangoFormImports import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from Models.BordjModels import *
#{%block imports%}
#{%endblock%}
###############

class DolgForm(ModelForm):
    class Meta():
        model=Dolg
        #exclude
##End Dolg
