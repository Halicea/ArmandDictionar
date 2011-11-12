from lib.djangoFormImports import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from Models.testModels import *
#{%block imports%}
#{%endblock%}
###############

class AnimalForm(ModelForm):
    class Meta():
        model=Animal
        #exclude
##End Animal
