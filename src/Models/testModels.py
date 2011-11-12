from google.appengine.ext import db
#{% block imports%}
#{%endblock%}
################
class Animal(db.Model):
    """TODO: Describe Animal"""
    Color= db.StringProperty()
    Name= db.StringProperty(required=True, )
    
    @classmethod
    def CreateNew(cls ,color,name , _isAutoInsert=False):
        result = cls(
                     Color=color,
                     Name=name,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End Animal
