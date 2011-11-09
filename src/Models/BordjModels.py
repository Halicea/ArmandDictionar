
from google.appengine.ext import db
#{% block imports%}
from BaseModels import Person
#{%endblock%}
################
class Dolg(db.Model):
    """TODO: Describe Dolg"""
    Od= db.ReferenceProperty(Person, required=True, collection_name='od_dolgs')
    Na= db.ReferenceProperty(Person, required=True, collection_name='na_dolgs')
    Kolicina= db.FloatProperty(required=True, )
    Datum= db.DateProperty(auto_now_add=True, )
    Note= db.TextProperty()
    DodadenOd = db.ReferenceProperty(Person, required=False, collection_name='dodaden_od_dolgs')
    Deleted = db.BooleanProperty(default=False)
    @classmethod
    def CreateNew(cls ,od,na,kolicina,note ,dodaden_od, _isAutoInsert=False):
        result = cls(
                     Od=od,
                     Na=na,
                     Kolicina=float(kolicina),
                     Note=note,
                     DodadenOd=dodaden_od)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Od.Name+' gave '+ self.Na.Name+' '+str(self.Kolicina)
## End Dolg

