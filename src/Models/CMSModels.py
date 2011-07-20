from google.appengine.ext import db
from BaseModels import Person
import datetime as dt
from lib.halicea.decorators import property

class CMSContent(db.Model):
    Title = db.StringProperty(required=True)
    HTMLContent = db.TextProperty(required=True)
    Tags = db.StringListProperty()
    Creator = db.ReferenceProperty(Person, collection_name='creator_cms_pages')
    DateCreated = db.DateTimeProperty(auto_now_add=True)
    LastDateModified = db.DateTimeProperty(auto_now=True)
    @classmethod
    def CreateNew(cls, title, content, tags, creator, _isAutoInsert=False):
        result = cls(
                    Title=title,
                    HTMLContent=content,
                    Tags=tags,
                    Creator=creator,
                   )
        if _isAutoInsert:
            result.put()
        return result

class ContentType:
    CMSPage = 0
    StaticPage = 1
    NoContent = 2 

class CMSLink(db.Model):
    AddressName = db.StringProperty(required=True)
    Name = db.StringProperty(required=True)
    ParentLink = db.SelfReferenceProperty(collection_name='parent_link_cms_links')
    Depth = db.IntegerProperty(required=True, default=0)
    Order = db.IntegerProperty(required=True, default=100)
    Content = db.ReferenceProperty(reference_class=CMSContent, collection_name='content_cms_links')
    Creator = db.ReferenceProperty(Person, collection_name='creator_cms_links')
    ContentTypeNumber = db.IntegerProperty(default = 0)
    DateCreated =db.DateTimeProperty(auto_now_add=True)
    LastDateModified =db.DateTimeProperty(auto_now=True)
    def GetChildren(self):
        return CMSLink.gql("WHERE Depth =:depth AND ParentLink =:pl", depth=self.Depth+1, pl=self).fetch(limit=1000)
    
    def GetTreeBelow(self):
        children = self.GetChildren()
        result = {}
        for child in children:
            result[child] = child.GetTreeBelow()
        return result
    
    @classmethod
    def GetLinkByPath(cls, path):
        items = [p for p in path.split('/') if p]
        curPar=None
        i=0
        for lnkStr in items:
            new_item = CMSLink.gql("WHERE Depth =:depth AND ParentLink =:pl AND AddressName =:address",depth=i, pl=curPar, address=lnkStr).get()
            if new_item: 
                curPar = new_item
            else:
                curPar = None
                break;
            i+=1;
        return curPar

    ###############################
    ## Static Methods 
  
    @staticmethod
    def GetLinksByDate(dateFrom, dateTo):
        return CMSLink.gql("WHERE LastDateModified > :ldf AND LastDateModified < :ldt ORDER BY LastDateModified ASC", ldf=dateFrom, ldt=dateTo).fetch(1000)
    @classmethod
    def CreateNew2(cls, addressName, name, parentLink, order, content, creator, _isAutoInsert=False):
        if not parentLink:
            depth = 0
        else:
            depth = parentLink.Depth+1
        result = cls(AddressName=addressName, Name=name, ParentLink=parentLink, Depth=depth, Order=order, Content=content, Creator=creator)
        if _isAutoInsert: result.put()
        return result
    
    @classmethod
    def GetLinkTree(cls):
        tree = cls.gql('WHERE Depth =:d', d=0).fetch(limit=1000, offset=0)
        result = {} 
        # get the root nodes
        for t in tree:
            result[t] = t.GetTreeBelow()
        return result
    ## End Static Methods

class Menu(db.Model):
    Name = db.StringProperty(required = True)
    Location = db.TextProperty(required = True)
    CssClass = db.StringProperty()
class Comment(db.Model):
    """TODO: Describe Comment"""
    Text= db.TextProperty(required=True, )
    Creator= db.ReferenceProperty(Person, collection_name='creator_comments', )
    DateAdded= db.DateTimeProperty(auto_now_add=True, )
    Content= db.ReferenceProperty(CMSContent, collection_name='content_comments', required=True, )
    
    @classmethod
    def CreateNew(cls ,text,creator,content , _isAutoInsert=False):
        result = cls(
                     Text=text,
                     Creator=creator,
                     Content=content,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End Comment
