# -*- coding: utf-8 -*-
import settings
from google.appengine.ext.db.djangoforms import ModelForm
from google.appengine.ext import db
from django.newforms import widgets, fields, extras
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
    def __str__(self):
        return self.Name+' '+self.Surname
class PersonForm(ModelForm):
    class Meta():
        model = Person
## End Person
##**************************

class WishList(db.Model):
    '''Whishes for the page look&feel and functionality '''
    Owner = db.ReferenceProperty(Person)
    Wish  = db.TextProperty()
    DateAdded = db.DateTimeProperty(auto_now_add=True)
    @classmethod
    def CreateNew(cls, owner, wish, _isAutoInsert=False):
        result = cls(Owner=owner, Wish=wish, DateAdded = dt.datetime.now())
        if _isAutoInsert: result.put()
        return result
    
    @classmethod
    def GetAll(cls, limit=1000, offset=0):
        return cls.all().fetch(limit=limit, offset=offset)
    
    def __str__(self):
        return self.Wish+'-'+self.Owner.__str__()
class WishListForm(ModelForm):
#    DateAdded = fields.DateField(widget=widgets.TextInput(attrs={'class':'date'}))
    class Meta():
        model=WishList
        exclude = ['Owner']
## End WishList
##**************************

class Role(db.Model):
    """TODO: Describe Role"""
    RoleName= db.StringProperty(required=True, )
    RoleDescription= db.TextProperty(required=True, )
    
    @classmethod
    def CreateNew(cls ,rolename,roledescription , _isAutoInsert=False):
        result = cls(
                     RoleName=rolename,
                     RoleDescription=roledescription,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.RoleName 
class RoleForm(ModelForm):
    class Meta():
        model=Role
## End Role
##**************************

class RoleAssociation(db.Model):
    """Association Class between Users and Roles"""
    Role= db.ReferenceProperty(Role, collection_name='role_roleassociations', )
    Person= db.ReferenceProperty(Person, collection_name='person_roleassociations', )

    @classmethod
    def CreateNew(cls ,rolename,roledescription,role,person , _isAutoInsert=False):
        result = cls(
                     Role=role,
                     Person=person,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Role.RoleName #+'-'+self.Person and self.Person.Name or 'None'+' '+self.Person and self.Person.Surname or 'None'
class RoleAssociationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleAssociationForm, self).__init__(*args, **kwargs)
        self.fields['Person'].queryset = Person.all().fetch(limit=100)
    class Meta():
        model=RoleAssociation
## End RoleAssociation
##**************************

