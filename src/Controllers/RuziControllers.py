import settings
from lib.HalRequestHandler import HalRequestHandler as hrh
from lib.decorators import *
from google.appengine.ext import db
##################################################
from Models.RuziModels import Boja, BojaForm 
class BojaController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='Boja_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'BojaList': Boja.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='Boja_shw.html')
        if self.params.key:
            item = Boja.get(self.params.key)
            if item:
                result = {'op':'upd', 'BojaForm': BojaForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Boja does not exists'
                self.redirect(BojaController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'BojaForm':BojaForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = Boja.get(self.params.key)
        form=BojaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Boja is saved'
            self.redirect(BojaController.get_url())
        else:
            self.SetTemplate(templateName = 'Boja_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'BojaForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Boja.get(self.params.key)
            if item:
                item.delete()
                self.status ='Boja is deleted!'
            else:
                self.status='Boja does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(BojaController.get_url())

from Models.RuziModels import Berba, BerbaForm 
class BerbaController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'show'}
    
    def list(self):
        self.SetTemplate(templateName='Berba_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'BerbaList': Berba.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='Berba_shw.html')
        if self.params.key:
            item = Berba.get(self.params.key)
            if item:
                bbl = item.berba_berbabojas.fetch(100)
                bb = BerbaBoja()
                bb.Berba =item
                bbf =  BerbaBojaForm(data={'Berba':item.key().__str__()})
                result = {'op':'upd', 
                          'BerbaForm': BerbaForm(instance=item),
                          'BerbaBojaList':bbl,
                          'BerbaBojaForm':bbf,
                          }
                self.respond(result)
            else:
                self.status = 'Berba does not exists'
                self.redirect(BerbaController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'BerbaForm':BerbaForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = Berba.get(self.params.key)
        form=BerbaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Berba is saved'
            self.redirect(BerbaController.get_url())
        else:
            self.SetTemplate(templateName = 'Berba_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'BerbaForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Berba.get(self.params.key)
            if item:
                item.delete()
                self.status ='Berba is deleted!'
            else:
                self.status='Berba does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(BerbaController.get_url())

from Models.RuziModels import BerbaBoja, BerbaBojaForm 
class BerbaBojaController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='BerbaBoja_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'BerbaBojaList': BerbaBoja.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='BerbaBoja_shw.html')
        if self.params.key:
            item = BerbaBoja.get(self.params.key)
            if item:
                result = {'op':'upd', 'BerbaBojaForm': BerbaBojaForm(instance=item)}
                self.redirect(BerbaController.get_url()+'?key='+item.Berba.key().__str__())
            else:
                self.status = 'BerbaBoja does not exists'
                self.redirect(BerbaController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'BerbaBojaForm':BerbaBojaForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = BerbaBoja.get(self.params.key)
        form=BerbaBojaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'BerbaBoja is saved'
            self.redirect(BerbaController.get_url()+'?key='+result.Berba.key().__str__())
        else:
            self.SetTemplate(templateName = 'BerbaBoja_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'BerbaBojaForm': form}
            self.respond(result)

    def delete(self):
        item = None
        respond_url = ''
        if self.params.key:
            item = BerbaBoja.get(self.params.key)
            respond_url = BerbaController.get_url()+'?key='+item.key().__str__()
            if item:
                item.delete()
                self.status ='BerbaBoja is deleted!'
            else:
                self.status='BerbaBoja does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(respond_url)

from Models.RuziModels import Preparat, PreparatForm 
class PreparatController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='Preparat_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'PreparatList': Preparat.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='Preparat_shw.html')
        if self.params.key:
            item = Preparat.get(self.params.key)
            if item:
                result = {'op':'upd', 'PreparatForm': PreparatForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Preparat does not exists'
                self.redirect(PreparatController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'PreparatForm':PreparatForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = Preparat.get(self.params.key)
        form=PreparatForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Preparat is saved'
            self.redirect(PreparatController.get_url())
        else:
            self.SetTemplate(templateName = 'Preparat_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'PreparatForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Preparat.get(self.params.key)
            if item:
                item.delete()
                self.status ='Preparat is deleted!'
            else:
                self.status='Preparat does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(PreparatController.get_url())

from Models.RuziModels import Zashtita, ZashtitaForm 
class ZashtitaController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='Zashtita_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'ZashtitaList': Zashtita.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='Zashtita_shw.html')
        if self.params.key:
            item = Zashtita.get(self.params.key)
            if item:
                result = {'op':'upd', 'ZashtitaForm': ZashtitaForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Zashtita does not exists'
                self.redirect(ZashtitaController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'ZashtitaForm':ZashtitaForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = Zashtita.get(self.params.key)
        form=ZashtitaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Zashtita is saved'
            self.redirect(ZashtitaController.get_url())
        else:
            self.SetTemplate(templateName = 'Zashtita_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'ZashtitaForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Zashtita.get(self.params.key)
            if item:
                item.delete()
                self.status ='Zashtita is deleted!'
            else:
                self.status='Zashtita does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(ZashtitaController.get_url())

from Models.RuziModels import Kupec, KupecForm 
class KupecController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='Kupec_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'KupecList': Kupec.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='Kupec_shw.html')
        if self.params.key:
            item = Kupec.get(self.params.key)
            if item:
                result = {'op':'upd', 'KupecForm': KupecForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Kupec does not exists'
                self.redirect(KupecController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'KupecForm':KupecForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = Kupec.get(self.params.key)
        form=KupecForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Kupec is saved'
            self.redirect(KupecController.get_url())
        else:
            self.SetTemplate(templateName = 'Kupec_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'KupecForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Kupec.get(self.params.key)
            if item:
                item.delete()
                self.status ='Kupec is deleted!'
            else:
                self.status='Kupec does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(KupecController.get_url())

from Models.RuziModels import Prodazba, ProdazbaForm 
class ProdazbaController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='Prodazba_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'ProdazbaList': Prodazba.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='Prodazba_shw.html')
        if self.params.key:
            item = Prodazba.get(self.params.key)
            if item:
                result = {'op':'upd', 'ProdazbaForm': ProdazbaForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Prodazba does not exists'
                self.redirect(ProdazbaController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'ProdazbaForm':ProdazbaForm()})


    def insert(self):
        instance = None
        if self.params.key:
            instance = Prodazba.get(self.params.key)
        form=ProdazbaForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Prodazba is saved'
            self.redirect(ProdazbaController.get_url())
        else:
            self.SetTemplate(templateName = 'Prodazba_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'ProdazbaForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = Prodazba.get(self.params.key)
            if item:
                item.delete()
                self.status ='Prodazba is deleted!'
            else:
                self.status='Prodazba does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(ProdazbaController.get_url())

