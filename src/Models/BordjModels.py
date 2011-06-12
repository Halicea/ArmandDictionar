import settings
from google.appengine.ext import db
#{% block imports%}
from BaseModels import Person
#{%endblock%}
################
class Dolg(db.Model):
    """TODO: Describe Dolg"""
    Od= db.ReferenceProperty(Person, required=True, collection_name='od_dolgs')
    Na= db.StringProperty(required=True, collection_name='na_dolgs')
    Kolicina= db.FloatProperty(required=True, )
    Datum= db.DateProperty(auto_now_add=True, )
    Note= db.TextProperty()
    @classmethod
    def CreateNew(cls ,od,na,kolicina,datum,note , _isAutoInsert=False):
        result = cls(
                     Od=od,
                     Na=na,
                     Kolicina=kolicina,
                     Datum=datum,
                     Note=note,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return Od.Name+' gave '+ Na.Name+' '+str(Kolicina)
## End Dolg

