import yaml
from lib.halicea.decorators import *
import Models.CMSModels as cms
from Controllers.BaseControllers import LoginController
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from Forms.CMSForms import CMSContentForm
from google.appengine.api import memcache
from lib import messages
from django.utils import simplejson
handlerType = "cms"
from urlparse import urlparse
def cr(request, methos, *args, **kwargs):
    request.request.Url = '/'
    getattr(request, 'view')(request, *args, **kwargs)
class CMSLinksController(hrh):
    @Handler(method='save', operation='save')
    def SetOperations(self):pass
    @AdminOnly()
    @View(templateName='CMSLinks.html')
    def index(self, *args):
        limit = 100
        offset = 0 
        try:
            offset = self.params.offset
        except:
            pass
        
        cmsLinks = cms.CMSLink.GetLinkTree()
        contents = cms.CMSContent.all().order('-DateCreated').fetch(limit=limit, offset=offset)
        return {'cmsLinks':cmsLinks, 'contents':contents}
    @AdminOnly()
    def save(self, *args):
        addressName = self.params.addressName
        name=self.params.name
        parent=self.params.parentLink
        if parent:
            parent = cms.CMSLink.get(parent)
        else:
            parent = None
        order= int(self.g('order'))
        content=self.g('content')
        if content:
            content = cms.CMSContent.get(content)
        creator= self.User
        cms.CMSLink.CreateNew2(addressName, name, parent, order, content, creator, _isAutoInsert=True)
        return self.index()
    @AdminOnly()
    def delete(self, *args):
        lnk=cms.CMSLink.get(self.params.key)
        if lnk:
            if lnk.Content.content_cms_links.count()==1:
                lnk.Content.delete()
            lnk.delete()
            self.status='Link is deleted'
            self.redirect(self.get_url())
        else:
            self.status="Link is invalid";
            self.redirect(self.get_url())

class CMSContentController(hrh):
    def __init__(self):
        super(CMSContentController, self).__init__()
        self.ContentForm = CMSContentForm()
    @Handler(operation='view', method='view')
    def SetOperations(self):pass


    def view(self, title, *args):
        cnt = cms.CMSContent.gql('WHERE Title = :t', t=title).fetch(1)
        if cnt:
            return {'content':cnt[0]}
        else:
            return cnt

    @View(templateName = 'CMSContent.html')
    def index(self, *args):
        limit = 10
        offset = 0 
        try:
            offset = int(self.params.offset)
        except:
            pass
        contents = cms.CMSContent.all().order('-DateCreated').fetch(limit=limit, offset=offset)
        return {'contents':contents}

    @AdminOnly()
    @Post()
    def save(self, *args):
        form = CMSContentForm(data=self.params)
        if form.is_valid():
            data =form.clean()
            tags = []
            try:
                tags = data['Tags'].split(',')
            except:
                pass
            cms.CMSContent.CreateNew(title=data['Title'], content=data['Content'], tags=tags, creator=self.User, _isAutoInsert=True)
            self.status ="Content is saved"
        else:
            self.status ='Content is Invalid'
            self.extra_context['op']=self.params.key and 'update' or 'insert'
            self.ContentForm = form
        return self.index()

    def edit(self, *args):
        if self.params.key:
            cmsContent = cms.CMSContent.get(self.params.key)
            self.ContentForm = CMSContentForm(instance=cmsContent)
        self.extra_context['op']=self.params.key and 'update' or 'insert'
        return {'CMSContentForm':self.ContentForm}

    @ErrorSafe(redirectUrl='/cms/content')
    def delete(self, *args):
        result = True
        if self.params.key:
            cms.CMSContent.get(self.params.key).delete()
            self.status='CMS Content has been deleted!'
        else:
            result=False
            self.status='Key Not Provided'
        if self.isAjax:
            return str(result)
        else:
            self.redirect(self.get_url())

class CMSPageController(hrh):
    @ClearDefaults()
    @Default('view')
    def SetOperations(self):pass
    
    def view(self, pagepath):
        lnk = cms.CMSLink.GetLinkByPath(pagepath)
        if lnk:
            return {'link':lnk}
        else:
            self.status ="Not Valid Page"
            self.redirect(LoginController.get_url())
#{%block imports%}
from Models.CMSModels import Comment
from Forms.CMSForms import CommentForm
#{%endblock%}
class CommentController(hrh):
    @Default('save')
    def SetOperations(self): pass
    
    def save(self, key):
        if self.params.Comment:
            Comment.CreateNew(self.params.Comment, self.User, cms.CMSContent.get(key), _isAutoInsert=True)
            self.status = 'Comment is saved'
        else:
            self.status = 'No Comment was given'
        if self.isAjax:
            simplejson.dumps({'status':self.status})
        else:
            self.redirect(CMSContentController.get_url(), permanent=True)

    def delete(self,*args):
        if self.params.key:
            item = Comment.get(self.params.key)
            if item:
                item.delete()
                self.status ='Comment is deleted!'
            else:
                self.status='Comment does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(CommentController.get_url())

    def index(self, *args):
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'CommentList': Comment.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def edit(self, *args):
        if self.params.key:
            item = Comment.get(self.params.key)
            if item:
                return {'op':'update', 'CommentForm': CommentForm(instance=item)}
            else:
                self.status = 'Comment does not exists'
                self.redirect(CommentController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'CommentForm':CommentForm()}
