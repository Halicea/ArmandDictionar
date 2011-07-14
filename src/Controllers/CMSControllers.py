'''
Created on Jan 31, 2010

@author: KMihajlov
'''
import yaml
from lib.halicea.decorators import *
import Models.CMSModels as cms
from Controllers.BaseControllers import LoginController
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from Forms.CMSForms import CMSContentForm
from google.appengine.api import memcache
from lib import messages
handlerType = "cms"

class CMSLinksController(hrh):
    @Handler(method='save', operation='save')
    def SetOperations(self):pass
    @AdminOnly()
    @View(templateName='CMSLinks.html')
    def index(self, *args):
        cmsLinks = cms.CMSLink.GetLinkTree()
        contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
        return {'cmsLinks':cmsLinks, 'contents':contents}
    @AdminOnly()
    def save(self, *args):
        addressName = self.params.addressName
        name = self.params.name
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
        cms.CMSLink.CreateNew(addressName, name, parent, order, content, creator, _isAutoInsert=True)
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

    @AdminOnly()
    @View(templateName = 'CMSContent.html')
    def index(self, *args):
        contents = cms.CMSContent.all().fetch(limit=1000, offset=0)
        return {'contents':contents, 'CMSContentForm':self.ContentForm}

    @AdminOnly()
    @Post()
    def save(self, *args):
        form = CMSContentForm(data=self.params)
        if form.is_valid():
            data =form.clean()
            cms.CMSContent.CreateNew(title=data['Title'], content=data['Content'], creator=self.User, _isAutoInsert=True)
            self.status ="Content is saved"
        else:
            self.status ='Content is Invalid'
            self.extra_context['op']='update'
            self.ContentForm = form
        return self.index()

    def edit(self, *args):
        if self.params.key:
            cmsContent = cms.CMSContent.get(self.params.key)
            self.ContentForm = CMSContentForm(instance=cmsContent)
            self.extra_context['op']='edit'
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
