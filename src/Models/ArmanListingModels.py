import settings
from google.appengine.ext import db
from Models.BaseModels import Person
#{% block imports%}
#{%endblock%}
################

class Address(db.Model):
    City =db.StringProperty(required=True)
    Municipality = db.StringProperty(required=True)
    Street = db.StringProperty()
    State = db.StringProperty()
    @classmethod
    def CreateNew(cls, city, municipality, street, zipcode, state, _isAutoInsert=False):
        result = cls(City=city, Municipality=municipality, Street=street, ZipCode=zipcode, State=state)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.City+'<br/>'+self.Municipality+'<br/>'+self.Street+'<br/>'+self.ZipCode.__str__()+'<br/>'+self.State+'<br/>'
    
class Arman(db.Model):
    """TODO: Describe Person"""
    MappedTo = db.ReferenceProperty(Person, required=False)
    Name = db.StringProperty(required=True)
    Surname = db.StringProperty(required=True)
    ArmanSurname= db.StringProperty()
    PersonalAddress = db.ReferenceProperty(Address, required=True, collection_name='personal_address_persons')
    #Email= db.EmailProperty()
    Email = db.StringProperty()
    Facebook= db.StringProperty()
    MobilePhone= db.PhoneNumberProperty()
    HomePhone= db.PhoneNumberProperty()
    IsSpeakingArman= db.BooleanProperty(default=True)
    IsWriteingArman= db.BooleanProperty()
    AddedBy = db.ReferenceProperty(Person, required=True, collection_name='added_by_armans')
    #DateAdded = db.DateTimeProperty(auto_now=True, auto_now_add=True)
    @classmethod
    def CreateNew(cls ,name,surname,armansurname, personalladress,
                  email,facebook,mobilephone,homephone,
                  isspeakingarman, iswriteingarman , 
                  _isAutoInsert=False):
        if not personalladress.key:
            personalladress.put()
        result = cls(Name=name,
                     Surname=surname,
                     ArmanSurname=armansurname,
                     PersonalAddress = personalladress,
                     Email=email,
                     Facebook=facebook,
                     MobilePhone=mobilephone,
                     HomePhone=homephone,
                     IsSpeakingArman=isspeakingarman,
                     IsWriteingArman=iswriteingarman,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Name+' '+self.Surname 
## End Person

    