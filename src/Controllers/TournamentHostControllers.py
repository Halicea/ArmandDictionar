# -*- coding: utf-8 -*-
import settings
from lib.HalRequestHandler import HalRequestHandler as hrh
from lib.decorators import *
from google.appengine.ext import db
##################################################
from Models.TournamentHostModels import Host, HostForm , Guest, GuestForm
class TournamentInfoController(hrh):
    def get(self):
        self.respond()
class HostController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'show'}
    
    def show(self):
        self.SetTemplate(templateName='Host_shw.html')
        if self.params.key:
            item = Host.get(self.params.key)
            if item:
                result = {'op':'upd', 'HostForm': HostForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Host does not exists'
                self.redirect(HostController.get_url())
        else:
            #self.status = 'Key not provided'
            self.respond({'op':'ins' ,'HostForm':HostForm()})

    @AdminOnly()
    def delete(self, *args):
        if self.params.key:
            item = Host.get(self.params.key)
            if item:
                item.delete()
                self.status ='Host is deleted!'
            else:
                self.status='Host does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(HostController.get_url())

    @AdminOnly()
    def list(self, *args):
        self.SetTemplate(templateName='Host_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        hosts = Host.all().fetch(limit=count, offset=index)
        TotalHosts = len(hosts)
        TotalPlaces = 0
        for t in hosts:
            TotalPlaces += t.BrojNaLugje
        result = {'HostList': hosts, 'TotalPlaces':TotalPlaces, 'TotalHosts':TotalHosts}
        #result.update(locals())
        self.respond(result)


    def insert(self):
        instance = None
        if self.params.key:
            instance = Host.get(self.params.key)
        form=HostForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = '<h3><b>Пријавата е зачувана, Ви благодариме на поддршката</b></h3>'
            self.redirect(HostController.get_url())
        else:
            self.SetTemplate(templateName = 'Host_shw.html')
            self.status = 'Формата на е валидна, ве молиме пополнете ги задолжителните полиња'
            result = {'op':'upd', 'HostForm': form}
            self.respond(result)

class GuestController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'show'}
    
    def show(self):
        self.SetTemplate(templateName='Guest_shw.html')
        if self.params.key:
            item = Guest.get(self.params.key)
            if item:
                result = {'op':'upd', 'GuestForm': GuestForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Guest does not exists'
                self.redirect(GuestController.get_url())
        else:
            #self.status = 'Key not provided'
            self.respond({'op':'ins' ,'GuestForm':GuestForm()})

    @AdminOnly()
    def delete(self, *args):
        if self.params.key:
            item = Guest.get(self.params.key)
            if item:
                item.delete()
                self.status ='Guest is deleted!'
            else:
                self.status='Guest does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(GuestController.get_url())

    @AdminOnly()
    def list(self, *args):
        self.SetTemplate(templateName='Guest_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        Guests = Guest.all().fetch(limit=count, offset=index)
        TotalGuestApplications = len(Guests)
        TotalGuests = 0
        for t in Guests:
            TotalGuests += t.BrojNaLugje
        result = {'GuestList': Guests, 'TotalGuestApplications':TotalGuestApplications, 'TotalGuests':TotalGuests}
        #result.update(locals())
        self.respond(result)


    def insert(self):
        instance = None
        if self.params.key:
            instance = Guest.get(self.params.key)
        form=GuestForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = '<h3><b>Application is saved, We are waiting for you.</b></h3>'
            self.redirect(GuestController.get_url())
        else:
            self.SetTemplate(templateName = 'Guest_shw.html')
            self.status = 'Form is not valid, you must fill all required fields'
            result = {'op':'upd', 'GuestForm': form}
            self.respond(result)
