
import datetime
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
from django.utils import simplejson as json
from google.appengine.ext import db
#{%block imports%}
from Models.stavModels import Rabotnik
from Forms.stavForms import RabotnikForm
from Models.stavModels import PlataZaMesec
from Forms.stavForms import PlataZaMesecForm
from Models.stavModels import Rezija
from Forms.stavForms import RezijaForm
from Models.stavModels import Nalog
from Forms.stavForms import NalogForm
from Models.stavModels import Partija
from Forms.stavForms import PartijaForm
from Models.stavModels import Rabota
from Forms.stavForms import RabotaForm
from Models.stavModels import Operacija
from Forms.stavForms import OperacijaForm
from lib.halicea import ContentTypes as ct
#{%endblock%}
################################

class RabotnikSearchController(hrh):
    @Default('search')
    @Handler(method='search', operation='search')
    @ResponseHeaders(**{'Content-Type':ct.JSON})
    def SetOperations(self):pass
    def search(self,*args):
        res = Rabotnik.gql("WHERE prop >= :1 AND prop < :2", self.params.q, self.params.q + u"\ufffd").fetch(100)[0].to_xml()
                
class RabotnikController(hrh):
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Rabotnik.get(self.params.key)
        form=RabotnikForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Rabotnik is saved'
            self.redirect(RabotnikController.get_url())
        else:
            self.SetTemplate(templateName = 'Rabotnik_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'RabotnikForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Rabotnik.get(self.params.key)
            if item:
                return {'op':'update', 'RabotnikForm': RabotnikForm(instance=item)}
            else:
                self.status = 'Rabotnik does not exists'
                self.redirect(RabotnikController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RabotnikForm':RabotnikForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Rabotnik_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'RabotnikList': Rabotnik.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Rabotnik.get(self.params.key)
            if item:
                item.delete()
                self.status ='Rabotnik is deleted!'
            else:
                self.status='Rabotnik does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(RabotnikController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Rabotnik.get(self.params.key)
            if item:
                return {'op':'update', 'RabotnikForm': RabotnikForm(instance=item)}
            else:
                self.status = 'Rabotnik does not exists'
                self.redirect(RabotnikController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RabotnikForm':RabotnikForm()}

class PlataZaMesecController(hrh):
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = PlataZaMesec.get(self.params.key)
        form=PlataZaMesecForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'PlataZaMesec is saved'
            self.redirect(PlataZaMesecController.get_url())
        else:
            self.SetTemplate(templateName = 'PlataZaMesec_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'PlataZaMesecForm': form}

    def edit(self, *args):
        if self.params.key:
            item = PlataZaMesec.get(self.params.key)
            if item:
                return {'op':'update', 'PlataZaMesecForm': PlataZaMesecForm(instance=item)}
            else:
                self.status = 'PlataZaMesec does not exists'
                self.redirect(PlataZaMesecController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'PlataZaMesecForm':PlataZaMesecForm()}

    @AdminOnly()
    @View(templateName='PlataZaMesec_index.html')
    def index(self, mesec=None,*args):
        if mesec:
            try:
                mesec = datetime.datetime.strptime(mesec, '%Y-%m-%d')
            except Exception, ex:
                self.status='Nevaliden Mesec'
                mesec = datetime.date.today()
        else:
            mesec = datetime.date.today()

        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count)
        listaZaMesec = PlataZaMesec.gql("WHERE Datum =:k", k=mesec).fetch(limit=count, offset=index)
        result = {'PlataZaMesecList': listaZaMesec}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = PlataZaMesec.get(self.params.key)
            if item:
                item.delete()
                self.status ='PlataZaMesec is deleted!'
            else:
                self.status='PlataZaMesec does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(PlataZaMesecController.get_url())

    def details(self, *args):
        if self.params.key:
            item = PlataZaMesec.get(self.params.key)
            if item:
                return {'op':'update', 'PlataZaMesecForm': PlataZaMesecForm(instance=item)}
            else:
                self.status = 'PlataZaMesec does not exists'
                self.redirect(PlataZaMesecController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'PlataZaMesecForm':PlataZaMesecForm()}

class RezijaController(hrh):
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Rezija.get(self.params.key)
        form=RezijaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Rezija is saved'
            self.redirect(RezijaController.get_url())
        else:
            self.SetTemplate(templateName = 'Rezija_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'RezijaForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Rezija.get(self.params.key)
            if item:
                return {'op':'update', 'RezijaForm': RezijaForm(instance=item)}
            else:
                self.status = 'Rezija does not exists'
                self.redirect(RezijaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RezijaForm':RezijaForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Rezija_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'RezijaList': Rezija.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Rezija.get(self.params.key)
            if item:
                item.delete()
                self.status ='Rezija is deleted!'
            else:
                self.status='Rezija does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(RezijaController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Rezija.get(self.params.key)
            if item:
                return {'op':'update', 'RezijaForm': RezijaForm(instance=item)}
            else:
                self.status = 'Rezija does not exists'
                self.redirect(RezijaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RezijaForm':RezijaForm()}

class NalogController(hrh):
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Nalog.get(self.params.key)
        form=NalogForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Nalog is saved'
            self.redirect(NalogController.get_url())
        else:
            self.SetTemplate(templateName = 'Nalog_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'NalogForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Nalog.get(self.params.key)
            if item:
                return {'op':'update', 'NalogForm': NalogForm(instance=item)}
            else:
                self.status = 'Nalog does not exists'
                self.redirect(NalogController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'NalogForm':NalogForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Nalog_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'NalogList': Nalog.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Nalog.get(self.params.key)
            if item:
                item.delete()
                self.status ='Nalog is deleted!'
            else:
                self.status='Nalog does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(NalogController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Nalog.get(self.params.key)
            if item:
                return {'op':'update', 'NalogForm': NalogForm(instance=item)}
            else:
                self.status = 'Nalog does not exists'
                self.redirect(NalogController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'NalogForm':NalogForm()}

class PartijaController(hrh):
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Partija.get(self.params.key)
        form=PartijaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Partija is saved'
            self.redirect(PartijaController.get_url())
        else:
            self.SetTemplate(templateName = 'Partija_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'PartijaForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Partija.get(self.params.key)
            if item:
                return {'op':'update', 'PartijaForm': PartijaForm(instance=item)}
            else:
                self.status = 'Partija does not exists'
                self.redirect(PartijaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'PartijaForm':PartijaForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Partija_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'PartijaList': Partija.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Partija.get(self.params.key)
            if item:
                item.delete()
                self.status ='Partija is deleted!'
            else:
                self.status='Partija does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(PartijaController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Partija.get(self.params.key)
            if item:
                return {'op':'update', 'PartijaForm': PartijaForm(instance=item)}
            else:
                self.status = 'Partija does not exists'
                self.redirect(PartijaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'PartijaForm':PartijaForm()}

class RabotaController(hrh):
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Rabota.get(self.params.key)
        form=RabotaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Rabota is saved'
            self.redirect(RabotaController.get_url())
        else:
            self.SetTemplate(templateName = 'Rabota_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'RabotaForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Rabota.get(self.params.key)
            if item:
                return {'op':'update', 'RabotaForm': RabotaForm(instance=item)}
            else:
                self.status = 'Rabota does not exists'
                self.redirect(RabotaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RabotaForm':RabotaForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Rabota_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'RabotaList': Rabota.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Rabota.get(self.params.key)
            if item:
                item.delete()
                self.status ='Rabota is deleted!'
            else:
                self.status='Rabota does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(RabotaController.get_url())

    def details(self, *args):
        if self.params.key:
            item = Rabota.get(self.params.key)
            if item:
                return {'op':'update', 'RabotaForm': RabotaForm(instance=item)}
            else:
                self.status = 'Rabota does not exists'
                self.redirect(RabotaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RabotaForm':RabotaForm()}

class OperacijaController(hrh):
    
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Operacija.get(self.params.key)
        form=OperacijaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Operacija is saved'
            self.redirect(OperacijaController.get_url())
        else:
            self.SetTemplate(templateName = 'Operacija_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'OperacijaForm': form}

    def edit(self, *args):
        if self.params.key:
            item = Operacija.get(self.params.key)
            if item:
                return {'op':'update', 'OperacijaForm': OperacijaForm(instance=item)}
            else:
                self.status = 'Operacija does not exists'
                self.redirect(OperacijaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'OperacijaForm':OperacijaForm()}

    def index(self, *args):
        self.SetTemplate(templateName="Operacija_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'OperacijaList': Operacija.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

    def delete(self,*args):
        if self.params.key:
            item = Operacija.get(self.params.key)
            if item:
                item.delete()
                self.status ='Operacija is deleted!'
            else:
                self.status='Operacija does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(OperacijaController.get_url())
    def details(self, *args):
        if self.params.key:
            item = Operacija.get(self.params.key)
            if item:
                return {'op':'update', 'OperacijaForm': OperacijaForm(instance=item)}
            else:
                self.status = 'Operacija does not exists'
                self.redirect(OperacijaController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'OperacijaForm':OperacijaForm()}
