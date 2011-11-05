from lib.paths import getViewsDict
from Models.BaseModels import Person
from google.appengine.api import mail
import settings
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
import os
#{%block imports%}
from Models.BordjModels import Dolg
from Forms.BordjForms import DolgForm
from lib.halicea import mobile_agents
#{%endblock%}
################################
class Totals(object):
    def __init__(self, dolgovi, user):
        self.dolzam = sum([x.Kolicina for x in dolgovi if str(x.Na.key()) == str(user.key())])
        self.dolzat = sum([x.Kolicina for x in dolgovi if str(x.Od.key()) == str(user.key())])
        self.balans = self.dolzat-self.dolzam

class DolgController(hrh):
    def SetOperations(self):
        super(DolgController, self).SetOperations()
        self.operations['default'] = {'method':self.index}
    @LogInRequired()
    def edit(self, *args):
        if self.params.key:
            item = Dolg.get(self.params.key)
            if item:
                type=0
                party = str(item.Od.key())
                if str(item.Od.key()) == str(self.User.key()):
                    type='1'
                    party = str(item.Na.key())
                form  = DolgForm(initial={'Type':type, 'Party':party, 'Note':item.Note, 'Ammount':int(item.Kolicina)})
                return {'op':'update', 'DolgForm':form, 'key':str(item.key())}
            else:
                self.status = 'Dolg does not exists'
                self.redirect(DolgController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'DolgForm':DolgForm()}

    @LogInRequired()
    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Dolg.get(self.params.key)
        form=DolgForm(data=self.request.POST)
        if form.is_valid():
            od = None
            na = None
            if  form.cleaned_data['Type']=='1':
                na = Person.get(form.cleaned_data['Party'])
                od = self.User
            else:
                od = Person.get(form.cleaned_data['Party'])
                na = self.User
            if instance:
                instance.Note = form.cleaned_data["Note"]
                instance.Kolicina = float(form.cleaned_data["Ammount"])
                instance.Od = od
                instance.Na = na
                instance.DodadenOd = self.User
                instance.put()
            else:
                instance = Dolg.CreateNew(od=od, na=na,
                                          kolicina= form.cleaned_data["Ammount"],
                                          note=form.cleaned_data["Note"],
                                          dodaden_od=self.User, _isAutoInsert=True)
            self.status = 'Dolg is saved'
            try:
                self.send_email(instance, self.get_edit_body(instance, nov=not self.params.key))
                self.status+=' and message is sent'
            except Exception, ex:
                import logging
                logging.error(ex.message)
                self.status+=' but message is not sent. Probably the party does not have an email added in the profile'
            self.redirect(DolgController.get_url())
        else:
            self.SetTemplate(templateName = 'Dolg_edit.html')
            self.status = 'Form is not Valid'
            return {'op':'update', 'DolgForm': form}

    @LogInRequired()
    def delete(self,*args):
        if self.params.key:
            item = Dolg.get(self.params.key)
            if item:
                item.Deleted = True
                item.put()
                self.status ='Dolg is deleted!'
                try:
                    self.send_email(item, self.get_delete_body(item))
                    self.status += ' Also mail was sent to the corresponding person'
                except Exception, ex:
                    self.status += ' Unfortunately mail was not sent to the corresponding person!'
            else:
                self.status='Dolg does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(DolgController.get_url())

    @LogInRequired()
    def details(self, *args):
        if self.params.key:
            item = Dolg.get(self.params.key)
            if item:
                form  = DolgForm()
                if item.Od == self.User:
                    form.cleaned_data['Type']=1
                    form.cleaned_data['Party'] = str(item.Na.key())
                else:
                    form.cleaned_data['Type']=0
                    form.cleaned_data['Party'] = str(item.Od.key())
                form.cleaned_data["Note"]=item.Note
                return {'op':'update', 'DolgForm': form}
            else:
                self.status = 'Dolg does not exists'
                self.redirect(DolgController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'DolgForm':DolgForm()}

    @LogInRequired()
    def index(self, *args):
        self.SetTemplate(templateName="Dolg_index.html")
        result ={}
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        if self.params.key:
            p=Person.get(self.params.key)
            d1 = Dolg.gql("WHERE Od = :me and Na = :on AND Deleted=False", me=self.User, on = p).fetch(limit=100, offset=0)
            d2 = Dolg.gql("WHERE Od = :on and Na = :me AND Deleted=False", me=self.User, on = p).fetch(limit=100, offset=0)
            result['DolgList']= d1+d2
            result['Party']=p
        else:
            result['DolgList'] = Dolg.gql('WHERE Od = :k AND Deleted=False', k=self.User).fetch(limit=count, offset=index)+Dolg.gql('WHERE Na = :k AND Deleted=False', k=self.User).fetch(limit=count, offset=index)
        result['Totals'] = Totals(result['DolgList'], self.User)
        result['DolgForm']= DolgForm();result['op']= 'update';
        result['DolgList'] = sorted(result['DolgList'], key=lambda x:x.Datum, reverse=True)
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count)
        from Forms.BaseForms import InvitationForm
        result['InvitationFormK'] = InvitationForm()
        result.update(locals())
        return result

    def get_edit_body(self, dolg, nov ):
        to = str(self.User.key())==str(dolg.Na.key()) and dolg.Od or dolg.Na
        tip  = str(self.User.key())==str(dolg.Na.key()) and 'Vi e Dolzen' or 'Mu Dolzite'
        zz = nov and 'vnese' or 'izmeni'
        return "Pocituvan/a "+ to.Name+",\n"+\
        self.User.Name+' '+self.User.Surname+' '+zz+' deka '+tip+' '+str(dolg.Kolicina)+' denari od datum '+str(dolg.Datum)+'.\n'+\
        "Porakata bese:"+dolg.Note+'\n------------------------------\n'+\
        "Ubav den, \n \t Halicea Admin."
    def get_delete_body(self, dolg ):
        to = str(self.User.key())==str(dolg.Na.key()) and dolg.Od or dolg.Na
        tip  = str(self.User.key())==dolg.Na and 'Vi e Dolzen' or 'Mu Dolzite'

        return "Pocituvan/a "+ to.Name+",\n"+\
        self.User.Name+' '+self.User.Surname+' go izbrisa dolgot->'+' deka '+tip+' '+str(dolg.Kolicina)+' denari od datum '+str(dolg.Datum)+'.\n'+\
        "Porakata bese:"+dolg.Note+'\n------------------------------\n'+\
        "Ubav den, \n \t Halicea Admin."

    def send_email(self, dolg, body):
        to = str(self.User.key())==str(dolg.Na.key()) and dolg.Od or dolg.Na
        mail.send_mail(sender="admin@halicea.com",
                      to=[to.Email,],
                      subject='[Smetki]'+self.User.Name+' '+self.User.Surname,
                      body=body
                      )