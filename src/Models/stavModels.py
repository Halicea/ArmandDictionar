import settings
from google.appengine.ext import db
#{% block imports%}
#{%endblock%}
################
class Rabotnik(db.Model):
    """TODO: Describe Rabotnik"""
    Ime= db.StringProperty(required=True, )
    Prezime= db.StringProperty(required=True, )
    Adresa= db.TextProperty()
    Tel= db.PhoneNumberProperty()
    
    @classmethod
    def CreateNew(cls ,ime,prezime,adresa,tel , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Prezime=prezime,
                     Adresa=adresa,
                     Tel=tel,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Ime+' '+self.Prezime
## End Rabotnik

class PlataZaMesec(db.Model):
    """TODO: Describe PlataZaMesec"""
    Rabotnik= db.ReferenceProperty(Rabotnik, collection_name='rabotnik_platazamesecs', required=True, )
    Plata= db.FloatProperty(required=True, )
    Datum= db.DateProperty(required=True, )
    
    @classmethod
    def CreateNew(cls ,rabotnik,plata,datum , _isAutoInsert=False):
        result = cls(
                     Rabotnik=rabotnik,
                     Plata=plata,
                     Datum=datum,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return str(self.Rabotnik)+'za '+str(self.Datum)+'=>'+str(self.Plata)
## End PlataZaMesec

class Rezija(db.Model):
    """TODO: Describe Rezija"""
    Rabotnik= db.ReferenceProperty(Rabotnik, collection_name='rabotnik_rezijas', required=True, )
    Saati= db.IntegerProperty(default=1, required=True, )
    Datum=db.DateProperty()
    @classmethod
    def CreateNew(cls ,rabotnik,saati,datum, _isAutoInsert=False):
        result = cls(
                     Rabotnik=rabotnik,
                     Saati=saati,
                     Datum=datum)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return str(self.Rabotnik)+'za '+str(self.Datum)+'=>'+str(self.Saati)+' saati'
## End Rezija

class Operacija(db.Model):
    """TODO: Describe Operacija"""
    Ime= db.StringProperty(required=True, )
    Cena= db.FloatProperty(required=True, )
    ValidnaDo= db.DateProperty()

    @classmethod
    def CreateNew(cls ,ime,cena,validnado , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Cena=cena,
                     ValidnaDo=validnado,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return self.Ime
## End Operacija

class Nalog(db.Model):
    """TODO: Describe Nalog"""
    Ime= db.StringProperty()
    Donesen= db.DateProperty()
    Start= db.DateProperty()
    Kraj= db.DateProperty()
    Operacii= db.ListProperty(item_type=db.Key, )
    
    @classmethod
    def CreateNew(cls ,ime,donesen,start,kraj,operacii , _isAutoInsert=False):
        result = cls(
                     Ime=ime,
                     Donesen=donesen,
                     Start=start,
                     Kraj=kraj,
                     Operacii=operacii,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return '%s donesen na %s '%(self.Ime, self.Donesen)
## End Nalog

class Partija(db.Model):
    """TODO: Describe Partija"""
    PartijaID= db.IntegerProperty()
    BrojKomadi= db.IntegerProperty()
    Nalog= db.ReferenceProperty(Nalog, collection_name='nalog_partijas', )
    
    @classmethod
    def CreateNew(cls ,partijaid,brojkomadi,nalog , _isAutoInsert=False):
        result = cls(
                     PartijaID=partijaid,
                     BrojKomadi=brojkomadi,
                     Nalog=nalog,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return "%s od nalog %s"%(self.PartijaID, self.Nalog)
## End Partija

class Rabota(db.Model):
    """TODO: Describe Rabota"""
    Rabotnik= db.ReferenceProperty(Rabotnik, collection_name='rabotnik_rabotas', )
    Nalog= db.ReferenceProperty(Nalog, collection_name='nalog_rabotas', )
    Operacija= db.ReferenceProperty(Operacija, collection_name='operacija_rabotas', )
    BrojKomadi= db.IntegerProperty()
    Datum= db.DateProperty()
    
    @classmethod
    def CreateNew(cls ,rabotnik,nalog,operacija,brojkomadi,datum , _isAutoInsert=False):
        result = cls(
                     Rabotnik=rabotnik,
                     Nalog=nalog,
                     Operacija=operacija,
                     BrojKomadi=brojkomadi,
                     Datum=datum,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        return "%s \tna datum %s za operacija %s \t napravil %s komadi."%(self.Rabotnik, self.Datum, self.Operacija, self.BrojKomadi)
## End Rabota


