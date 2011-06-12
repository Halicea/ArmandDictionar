import settings
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
from google.appengine.ext import db
#{%block imports%}
from Models.BordjModels import Dolg
from Forms.BordjForms import DolgForm
#{%endblock%}
################################

class DolgController(hrh):
    
    def edit(self, *args):
        if self.params.key:
            item = Dolg.get(self.params.key)
            if item:
                return {'op':'update', 'DolgForm': DolgForm(instance=item)}
            else:
                self.status = 'Dolg does not exists'
                self.redirect(DolgController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'DolgForm':DolgForm()}

    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Dolg.get(self.params.key)
        form=DolgForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Dolg is saved'
            self.redirect(DolgController.get_url())
        else:
            self.SetTemplate(templateName = 'Dolg_shw.html')
            self.status = 'Form is not Valid'
            return {'op':'upd', 'DolgForm': form}

    def delete(self,*args):
        if self.params.key:
            item = Dolg.get(self.params.key)
            if item:
                item.delete()
                self.status ='Dolg is deleted!'
            else:
                self.status='Dolg does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(DolgController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Dolg.get(self.params.key)
            if item:
                return {'op':'upd', 'DolgForm': DolgForm(instance=item)}
            else:
                self.status = 'Dolg does not exists'
                self.redirect(DolgController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'ins' ,'DolgForm':DolgForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Dolg_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'DolgList': Dolg.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result
