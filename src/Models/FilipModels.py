import settings
from google.appengine.ext import db
#{% block imports%}
#{%endblock%}
################
class Konj(db.Model):
    """TODO: Describe Konj"""
    Ime= db.StringProperty(required=True)
    Prezime= db.StringProperty(required=True, )
    
    @classmethod
    def CreateNew(cls ,ime,prezime , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Prezime=prezime,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Ime+' '+self.Prezime 
## End Konj
