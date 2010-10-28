import settings
from google.appengine.ext.db.djangoforms import ModelForm
from google.appengine.ext import db
from django.newforms import widgets, fields, extras
##################################################

class Mdl(db.Model):
    """TODO: Describe Mdl"""
    p1= db.IntegerProperty()
    p2= db.StringProperty()
    
    @classmethod
    def CreateNew(cls ,p1,p2 , _isAutoInsert=False):
        result = cls(
                     p1=p1,
                     p2=p2,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
class MdlForm(ModelForm):
    class Meta():
        model=Mdl
        #exclude
## End Mdl
##**************************
