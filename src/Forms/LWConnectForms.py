from lib.djangoFormImports import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from Models.LWConnectModels import *
#{%block imports%}
#{%endblock%}
###############

class SprintForm(ModelForm):
    class Meta():
        model=Sprint
        #exclude
##End Sprint
def get_valid_choices():
    return set([(x, x) for x in Statuses if x!='Created'])
class BranchForm(ModelForm):
    Status = fields.ComboField(widget =widgets.Select(choices= get_valid_choices()))
    class Meta():
        model=Branch
        #exclude
##End Branch

class ActivityLogForm(ModelForm):
    class Meta():
        model=ActivityLog
        #exclude
##End ActivityLog