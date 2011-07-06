import settings
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
import inspect
from google.appengine.ext import db
#{%block imports%}
from Models.LWConnectModels import Sprint
from Forms.LWConnectForms import SprintForm
from Models.LWConnectModels import Branch
from Forms.LWConnectForms import BranchForm
from Models.LWConnectModels import ActivityLog
from Forms.LWConnectForms import ActivityLogForm
#{%endblock%}
################################
class LogedActivity(object):
    def __init__(self):
        pass
    def __call__(self, f):
        def new_f(request, *args, **kwargs):
            ActivityLog.CreateNew(request.__class__.__name__, f.__name__,request.User.UserName, True)
            return f(request, *args, **kwargs)
        return new_f

class SprintController(hrh):
    @LogInRequired()
    @LogedActivity()
    @Handler('POST', 'GET')
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Sprint.get(self.params.key)
        form=SprintForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Sprint is saved'
            self.redirect(SprintController.get_url())
        else:
            self.SetTemplate(templateName = 'Sprint_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'SprintForm': form}

    @LogInRequired()
    def edit(self, *args):
        if self.params.key:
            item = Sprint.get(self.params.key)
            if item:
                return {'op':'update', 'SprintForm': SprintForm(instance=item)}
            else:
                self.status = 'Sprint does not exists'
                self.redirect(SprintController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'SprintForm':SprintForm()}

    @LogInRequired()
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
        result = {'SprintList': Sprint.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    @LogInRequired()
    @LogedActivity()
    def delete(self,*args):
        if self.params.key:
            item = Sprint.get(self.params.key)
            if item:
                item.delete()
                self.status ='Sprint is deleted!'
            else:
                self.status='Sprint does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(SprintController.get_url())

    @LogInRequired()
    def details(self, *args):
        if self.params.key:
            item = Sprint.get(self.params.key)
            if item:
                return {'Sprint': item}
            else:
                self.status = 'Sprint does not exists'
                self.redirect(SprintController.get_url())
        else:
            self.status = 'Key not provided'
            self.redirect(SprintController.get_url())

class BranchController(hrh):
    @LogInRequired()
    @LogedActivity()
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Branch.get(self.params.key)
        form=BranchForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Branch is saved'
            self.redirect(BranchController.get_url())
        else:
            self.SetTemplate(templateName = 'Branch_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'BranchForm': form}

    @LogInRequired()
    def edit(self, *args):
        if self.params.key:
            item = Branch.get(self.params.key)
            if item:
                return {'op':'update', 'BranchForm': BranchForm(instance=item)}
            else:
                self.status = 'Branch does not exists'
                self.redirect(BranchController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'BranchForm':BranchForm()}

    @LogInRequired()
    def index(self, *args):
        self.SetTemplate(templateName="Branch_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'BranchList': Branch.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    @LogInRequired()
    @LogedActivity()
    def delete(self,*args):
        if self.params.key:
            item = Branch.get(self.params.key)
            if item:
                item.delete()
                self.status ='Branch is deleted!'
            else:
                self.status='Branch does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(BranchController.get_url())

    @LogInRequired()
    def details(self, *args):
        if self.params.key:
            item = Branch.get(self.params.key)
            if item:
                return {'op':'update', 'BranchForm': BranchForm(instance=item)}
            else:
                self.status = 'Branch does not exists'
                self.redirect(BranchController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'BranchForm':BranchForm()}

class ActivityLogController(hrh):
    @AdminOnly()
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = ActivityLog.get(self.params.key)
        form=ActivityLogForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'ActivityLog is saved'
            self.redirect(ActivityLogController.get_url())
        else:
            self.SetTemplate(templateName = 'ActivityLog_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'ActivityLogForm': form}

    @AdminOnly()
    def edit(self, *args):
        if self.params.key:
            item = ActivityLog.get(self.params.key)
            if item:
                return {'op':'update', 'ActivityLogForm': ActivityLogForm(instance=item)}
            else:
                self.status = 'ActivityLog does not exists'
                self.redirect(ActivityLogController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'ActivityLogForm':ActivityLogForm()}

    @AdminOnly()
    def index(self, *args):
        self.SetTemplate(templateName="ActivityLog_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'ActivityLogList': ActivityLog.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    @AdminOnly()
    def delete(self,*args):
        if self.params.key:
            item = ActivityLog.get(self.params.key)
            if item:
                item.delete()
                self.status ='ActivityLog is deleted!'
            else:
                self.status='ActivityLog does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(ActivityLogController.get_url())

    @AdminOnly()
    def details(self, *args):
        if self.params.key:
            item = ActivityLog.get(self.params.key)
            if item:
                return {'op':'update', 'ActivityLogForm': ActivityLogForm(instance=item)}
            else:
                self.status = 'ActivityLog does not exists'
                self.redirect(ActivityLogController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'ActivityLogForm':ActivityLogForm()}
