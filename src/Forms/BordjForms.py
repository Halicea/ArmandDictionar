from lib.djangoFormImports import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from django.newforms import Form
from Models.BordjModels import *
#{%block imports%}
#{%endblock%}
###############
def get_people():
    return [[str(x.key()), x.Name+' '+x.Surname] for x in Person.all().fetch(limit=100, offset=0)]

class DolgForm(Form):
    Type = fields.ChoiceField(choices=((0,'Mu Dolzam'), (1,'Mi Dolzi')), required=True,
                              widget=widgets.RadioSelect(attrs={'style':'display: inline;margin-left: 0.5em;'})
    )
    Party = fields.ComboField(required=True, widget=widgets.Select(choices=get_people()))
    Ammount = fields.IntegerField(required=True)
    Note = fields.Field(widget= widgets.Textarea)
    #To = fields.ComboField(widget=widgets.Select(choices=[(x.Name, str(x.key())) for x in Person.all().fetch(offset=0,limit=100)]))

##End Dolg
