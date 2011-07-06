from datetime import datetime
import settings
from google.appengine.ext import db
#{% block imports%}
from Models.BaseModels import Person
#{%endblock%}
################
Statuses =(
    'Merged Into Main',
    'Deleted',
    'Created',
)
Categories = (
    'Prototype', 'Part of Sprint', 'Experimentation',
)
class Sprint(db.Model):
    """TODO: Describe Sprint"""
    Name= db.StringProperty(required=True, )
    StartDate= db.DateProperty()
    EndDate= db.DateProperty()
    def get_branches(self):
        return self.sprint_branches
    Branches = property(get_branches)
    @classmethod
    def CreateNew(cls ,name,startdate,enddate , _isAutoInsert=False):
        result = cls(
                     Name=name,
                     StartDate=startdate,
                     EndDate=enddate,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Name+'('+str(self.StartDate)+'-'+str(self.EndDate)+')'
## End Sprint

class Branch(db.Model):
    """TODO: Describe Branch"""
    Name= db.StringProperty(default='No Name')
    LastSyncDate= db.DateProperty()
    Owner= db.ReferenceProperty(Person, required=True, collection_name='owner_branches', )
    Sprint = db.ReferenceProperty(Sprint, collection_name='sprint_branches')
    Status = db.StringProperty(choices=Statuses, required=True)
    Category = db.StringProperty(choices=Categories, required=True)
    @classmethod
    def CreateNew(cls ,name,lastsyncdate,owner, category , _isAutoInsert=False):
        result = cls(Name=name,
                     LastSyncDate=lastsyncdate,
                     Owner=owner,
                     Status='Created',
                     Category=category)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Name+'('+self.Owner.Name+')'+'-'+str(self.LastSyncDate)
## End Branch
class BranchHistory(db.Model):
    Branch = db.ReferenceProperty(Branch, required=True, collection_name='branch_history')
    StatusFrom = db.StringProperty()
    StatusTo = db.StringProperty()
    Date = db.DateProperty(auto_now_add=True)
    ModifyUser = db.ReferenceProperty(Person, required=True)
    @classmethod
    def CreateNew(cls, branch, statusfrom, statusto, _isAutoInsert=False):
        result = cls(Branch=branch, StatusFrom = statusfrom, StatusTo = statusto )
        if _isAutoInsert:
            result.put()
        return result
    def __str__(self):
        return self.Branch.BranchName+ 'modfied to '+self.StatusTo.Name+' from '+self.StatusFrom.Name+' by '+self.ModifyUser.UserName
class ActivityLog(db.Model):
    """TODO: Describe ActivityLog"""
    ResourceName= db.StringProperty()
    ResourceAction= db.StringProperty()
    ActionTime= db.DateTimeProperty(auto_now_add=True, )
    UserName= db.StringProperty()
    
    @classmethod
    def CreateNew(cls ,resourcename,resourceaction,username , _isAutoInsert=False):
        result = cls(
                     ResourceName=resourcename,
                     ResourceAction=resourceaction,
                     ActionTime=datetime.now(),
                     UserName=username,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.ResourceName+' '+self.ResourceAction+' performed by '+self.UserName+' on '+str(self.ActionTime)
## End ActivityLog