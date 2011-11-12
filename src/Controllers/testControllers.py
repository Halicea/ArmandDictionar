from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
from google.appengine.ext import db
#{%block imports%}
from Models.testModels import Animal
from Forms.testForms import AnimalForm
#{%endblock%}
################################

class AnimalController(hrh):
    def SetOperations(self): pass
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Animal.get(self.params.key)
        form=AnimalForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Animal is saved'
            self.redirect(AnimalController.get_url())
        else:
            self.SetTemplate(templateName = 'Animal_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'AnimalForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Animal.get(self.params.key)
            if item:
                return {'op':'update', 'AnimalForm': AnimalForm(instance=item)}
            else:
                self.status = 'Animal does not exists'
                self.redirect(AnimalController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'AnimalForm':AnimalForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Animal_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'AnimalList': Animal.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Animal.get(self.params.key)
            if item:
                item.delete()
                self.status ='Animal is deleted!'
            else:
                self.status='Animal does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(AnimalController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Animal.get(self.params.key)
            if item:
                return {'Animal': Animal}
            else:
                self.status = 'Animal does not exists'
                self.redirect(AnimalController.get_url())
        else:
            self.status = 'Key not provided'
            return {'Animal':Animal}
