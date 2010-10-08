# -*- coding: utf-8 -*-
import settings
from google.appengine.ext.db.djangoforms import ModelForm
from google.appengine.ext.db import djangoforms as df 
from google.appengine.ext import db
from django.newforms.fields import ChoiceField, EmailField, Field 
from django.newforms.widgets import RadioSelect, Textarea
##################################################

class Host(db.Model):
    """TODO: Describe Host"""
    Ime= db.StringProperty()
    Prezime= db.StringProperty()
    Telefon= db.StringProperty()
    Email = db.EmailProperty()
    Adresa= db.TextProperty()
    BrojNaLugje= db.IntegerProperty()
    Tip = db.StringProperty()
    Komentar = db.TextProperty()
    @classmethod
    def CreateNew(cls ,ime,prezime,telefon,email,adresa,brojnalugje , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Prezime=prezime,
                     Telefon=telefon,
                     Email = email,
                     Adresa=adresa,
                     BrojNaLugje=brojnalugje,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Ime+' '+self.Prezime+'('+self.Telefon+' | '+self.Email+')'+'     '+str(self.BrojNaLugje) 

class HostForm(ModelForm):
    Ime = Field(required=True, label='Име' )
    Prezime = Field(required=True, label='Презиме' )
    Telefon = Field(required=True, label='Телефон' )
    Email = EmailField(max_length=100, min_length=5)
    BrojNaLugje = ChoiceField( required=True, label='Број на луѓе', help_text='Колку гости би можеле да примите?',
                               choices=[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]] ,
                               initial=2)
    Tip = ChoiceField(required=True, label='Тип' ,
                      widget=RadioSelect, 
                      choices=[['Male','Male'], ['Female', 'Female'],['Couple', 'Couple'], ['Any', 'Any']], 
                      initial='Any')
    Adresa = Field(required=False, widget=Textarea, label='Aдреса')
    Komentar = Field(required=False, widget=Textarea, label='Дополнителен Коментар')
    class Meta():
        model=Host
        #exclude
## End Host
##**************************

class Guest(db.Model):
    """TODO: Describe Host"""
    Ime= db.StringProperty()
    Prezime= db.StringProperty()
    Telefon= db.StringProperty()
    Email = db.EmailProperty()
    BrojNaLugje= db.IntegerProperty()
    Tip = db.StringProperty()
    Komentar = db.TextProperty()
    @classmethod
    def CreateNew(cls ,ime,prezime,telefon,email,adresa,brojnalugje , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Prezime=prezime,
                     Telefon=telefon,
                     Email = email,
                     Adresa=adresa,
                     BrojNaLugje=brojnalugje,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Ime+' '+self.Prezime+'('+self.Telefon+' | '+self.Email+')'+'     '+str(self.BrojNaLugje) 

class GuestForm(ModelForm):
    Ime = Field(required=True, label='Name' )
    Prezime = Field(required=True, label='Surname' )
    Telefon = Field(required=True, label='Telephone' )
    Email = EmailField(max_length=100, min_length=5)
    BrojNaLugje = ChoiceField( required=True, label='Number of People coming', help_text='How many pople are you?',
                               choices=[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]] ,
                               initial=2)
    Tip = ChoiceField(required=True, label='Type' ,
                      widget=RadioSelect, 
                      choices=[['Male','Male'], ['Female', 'Female'],['Couple', 'Couple'], ['Mixed', 'Mixed']], 
                      initial='Mixed')
    Komentar = Field(required=False, widget=Textarea, label='Additional Comment')
    class Meta():
        model=Guest
        #exclude
## End Host
##**************************