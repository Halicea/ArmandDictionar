'''
Created on Jul 21, 2009

@author: Kosta
'''
###########
from google.appengine.ext import db
import datetime as dt
###########

class Person(db.Model):
    '''A Person with UserName, Name, Surname Phone Email e.t.c'''
    UserName = db.StringProperty(required=True)
    Password = db.StringProperty(required=True)
    Name = db.StringProperty(required=True)
    Surname = db.StringProperty(required=True)
    Email = db.EmailProperty(required=True)
    Public = db.BooleanProperty(default=True)
    Notify = db.BooleanProperty(default=False)
    DateAdded = db.DateTimeProperty()
    IsAdmin = db.BooleanProperty(default=False)

    def put(self):
        _isValid_, _error_ = self.__validate__()
        if(_isValid_):
            if not self.is_saved():
                self.DateAdded = dt.datetime.now()
            super(Person, self).put()
        else:
            raise Exception(_error_)

    def __validate__(self):
        __errors__ = []
        if not self.UserName or len(self.UserName)<3:
            __errors__.append('UserName must not be less than 3 characters')
        if not self.Email: #or self.Email.validate('^[0-9,a-z,A-Z,.]+@[0-9,a-z,A-Z].[com, net, org]'):
            __errors__.append('Email Must Not be Empty')
        if len(self.Password) < 6  or str(self.Password).find(self.Name) >= 0:
            __errors__.append('Not a good Password(Must be at least 6 characters long, and not containing your name')

        return not __errors__ and (True, None) or (False, ' and\r\n'.join(__errors__))

    @classmethod
    def CreateNew(csl, uname, name, surname, email, password, public, notify, _autoSave=False):
        result = cls(UserName = uname,
                    Email=email,
                    Name=name,
                    Surname=surname,
                    Password=password,
                    Public=public,
                    Notify=notify
                    )
        if _autoSave:
            result.put()
        return result
    @classmethod
    def GetUser(cls, uname, password):
        u = None
        if '@' in uname:
            u = cls.gql('WHERE Password= :passwd AND Email= :uname', uname=uname, passwd=password).get()
        else:
            u = cls.gql('WHERE Password= :passwd AND UserName= :uname', uname=uname, passwd=password).get()
        return u
#TODO; Implement this class
#TODO: Associate privileges class(need to make that as well
class Role(db.Model):
    RoleName = db.StringProperty(required=True)
    RoleDescription = db.TextProperty(required=True)

class RoleAssciation(db.Model):
    Role = db.ReferenceProperty(Role, collection_name='role_role_associations')
    Person = db.ReferenceProperty(Person,collection_name='person_person_associations')
    
    @classmethod
    def CreateNew(cls, person, role, _isAutoInsert=False):
        result = cls(Person=person, Role=role)
        if _isAutoInsert: result.put()
        return result 

class WishList(db.Model):
    '''Whishes for the page look&feel and functionality '''
    Owner = db.ReferenceProperty(Person)
    Wish  = db.TextProperty()
    DateAdded = db.DateTimeProperty()
    @classmethod
    def CreateNew(cls, owner, wish, _isAutoInsert=False):
        result = cls(Owner=owner, Wish=wish, DateAdded = dt.datetime.now())
        if _isAutoInsert: result.put()
        return result
    
    @classmethod
    def GetAll(cls, limit=1000, offset=0):
        return cls.all().fetch(limit=limit, offset=offset)
