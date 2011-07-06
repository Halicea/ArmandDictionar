from lib.djangoFormImports import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from Models.stavModels import *
#{%block imports%}
#{%endblock%}
###############

class RabotnikForm(ModelForm):
    class Meta():
        model=Rabotnik
        #exclude
##End Rabotnik

class PlataZaMesecForm(ModelForm):
    class Meta():
        model=PlataZaMesec
        #exclude
##End PlataZaMesec

class RezijaForm(ModelForm):
    class Meta():
        model=Rezija
        #exclude
##End Rezija

class NalogForm(ModelForm):
    class Meta():
        model=Nalog
        #exclude
##End Nalog

class PartijaForm(ModelForm):
    class Meta():
        model=Partija
        #exclude
##End Partija

class RabotaForm(ModelForm):
    class Meta():
        model=Rabota
        #exclude
##End Rabota

class OperacijaForm(ModelForm):
    class Meta():
        model=Operacija
        #exclude
##End Operacija
