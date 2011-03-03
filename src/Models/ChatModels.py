import settings
from google.appengine.ext import db
#{% block imports%}
#{%endblock%}
################
class User(db.Model):
    """TODO: Describe User"""
    Name= db.StringProperty(required=True, )
    
    @classmethod
    def CreateNew(cls ,name , _isAutoInsert=False):
        result = cls(
                     Name=name,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End User


class Room(db.Model):
    """TODO: Describe Room"""
    Name= db.StringProperty()
    CreatedBy= db.ReferenceProperty(User, collection_name='createdby_rooms', )
    
    @classmethod
    def CreateNew(cls ,name,createdby , _isAutoInsert=False):
        result = cls(
                     Name=name,
                     CreatedBy=createdby,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End Room


class UserInRoom(db.Model):
    """TODO: Describe UserInRoom"""
    Which= db.ReferenceProperty(User, collection_name='which_userinrooms', required=True, )
    Where= db.ReferenceProperty(Room, collection_name='where_userinrooms', required=True, )
    
    @classmethod
    def CreateNew(cls ,which,where , _isAutoInsert=False):
        result = cls(
                     Which=which,
                     Where=where,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End UserInRoom


class Message(db.Model):
    """TODO: Describe Message"""
    MessageContent= db.StringProperty()
    FromUser= db.ReferenceProperty(User, collection_name='fromuser_messages', required=True, )
    ToRoom= db.ReferenceProperty(Room, collection_name='toroom_messages', required=True, )
    DateSent= db.DateProperty()
    
    @classmethod
    def CreateNew(cls ,messagecontent,fromuser,toroom,datesent , _isAutoInsert=False):
        result = cls(
                     MessageContent=messagecontent,
                     FromUser=fromuser,
                     ToRoom=toroom,
                     DateSent=datesent,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End Message

