# -*- coding: utf-8 -*-
import settings
from google.appengine.ext.db.djangoforms import ModelForm
from google.appengine.ext import db
from django.newforms import widgets, fields, extras
from datetime import date
##################################################

class Boja(db.Model):
    """TODO: Describe Boja"""
    ImeBoja= db.StringProperty()
    
    @classmethod
    def CreateNew(cls ,imeboja , _isAutoInsert=False):
        result = cls(
                     ImeBoja=imeboja,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.ImeBoja
class BojaForm(ModelForm):
    class Meta():
        model=Boja
        #exclude
## End Boja
##**************************

class Berba(db.Model):
    """TODO: Describe Berba"""
    Datum= db.DateProperty()
    
    @classmethod
    def CreateNew(cls ,datum , _isAutoInsert=False):
        result = cls(
                     Datum=datum,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return str(self.Datum) 
class BerbaForm(ModelForm):
    Datum = fields.DateField(widget=widgets.TextInput(attrs={'class':'date'}))
    class Meta():
        model=Berba
        #exclude
## End Berba
##**************************

class BerbaBoja(db.Model):
    """TODO: Describe BerbaBoja"""
    Berba= db.ReferenceProperty(Berba, collection_name='berba_berbabojas', )
    Boja= db.ReferenceProperty(Boja, collection_name='boja_berbabojas', )
    Komadi= db.IntegerProperty()
    
    @classmethod
    def CreateNew(cls ,berba,boja,komadi , _isAutoInsert=False):
        result = cls(
                     Berba=berba,
                     Boja=boja,
                     Komadi=komadi,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return str(self.Boja)+'-'+str(self.Komadi) 
class BerbaBojaForm(ModelForm):
    class Meta():
        model=BerbaBoja
        #exclude
## End BerbaBoja
##**************************

class Preparat(db.Model):
    """TODO: Describe Preparat"""
    ImePreparat= db.StringProperty()
    @classmethod
    def CreateNew(cls ,imepreparat,ime , _isAutoInsert=False):
        result = cls(
                     ImePreparat=imepreparat,
                     )
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.ImePreparat 
class PreparatForm(ModelForm):
    class Meta():
        model=Preparat
        #exclude
## End Preparat
##**************************

class Zashtita(db.Model):
    """TODO: Describe Zashtita"""
    Preparat= db.ReferenceProperty(Preparat, collection_name='preparat_zashtitas', )
    Datum= db.DateProperty()
    KolichinaLitri= db.IntegerProperty()
    
    @classmethod
    def CreateNew(cls ,imepreparat,ime,preparat,datum,kolichinalitri , _isAutoInsert=False):
        result = cls(
                     Preparat=preparat,
                     Datum=datum,
                     KolichinaLitri=kolichinalitri,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return str(self.Datum)+'-'+str(self.Preparat)+'-'+str(self.KolichinaLitri) 
class ZashtitaForm(ModelForm):
    Datum = fields.DateField(widget=widgets.TextInput(attrs={'class':'date'}))
    class Meta():
        model=Zashtita
        #exclude
## End Zashtita
##**************************

class Kupec(db.Model):
    """TODO: Describe Kupec"""
    Ime= db.StringProperty()
    Telefon= db.StringProperty()
    Adresa= db.TextProperty()
    
    @classmethod
    def CreateNew(cls ,ime,telefon,adresa , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Telefon=telefon,
                     Adresa=adresa,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Ime
class KupecForm(ModelForm):
    class Meta():
        model=Kupec
        #exclude
## End Kupec
##**************************

class Prodazba(db.Model):
    """TODO: Describe Prodazba"""
    Kupec= db.ReferenceProperty(Kupec, collection_name='kupec_prodazbas', )
    TipRuza= db.ReferenceProperty(Boja, collection_name='tipruza_prodazbas', )
    Koliina= db.IntegerProperty()
    VkupnoCena= db.IntegerProperty()
    Dostaveno= db.BooleanProperty()
    Plateno= db.BooleanProperty()
    Datum = db.DateProperty(auto_now_add=True)
    @classmethod
    def CreateNew(cls ,kupec,tipruza,koliina,vkupnocena,dostaveno,plateno , _isAutoInsert=False):
        result = cls(
                     Kupec=kupec,
                     TipRuza=tipruza,
                     Koliina=koliina,
                     VkupnoCena=vkupnocena,
                     Dostaveno=dostaveno,
                     Plateno=plateno,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return str(self.Kupec)+' '+(self.Plateno and 'Plateno' or 'Neplateno')
class ProdazbaForm(ModelForm):
    Datum = fields.DateField(initial=date.today(), widget=widgets.TextInput(attrs={'class':'date'}))
    class Meta():
        model=Prodazba
        #exclude
## End Prodazba
##**************************
