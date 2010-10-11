# -*- coding: utf-8 -*-
import settings
from google.appengine.ext.db.djangoforms import ModelForm
from google.appengine.ext import db
from datetime import date
import re, htmlentitydefs
import logging
from BaseModels import Person
from django.newforms.fields import ChoiceField, EmailField, Field
from django.newforms.widgets import RadioSelect, Textarea
va =u'ã'
rpl ={u'â':va, u'Ã£':va, u'ã':va}
##################################################
batchImporterCode = 'Batch'
class Importer(db.Model):
    Code = db.StringProperty(required=True)
    Person = db.ReferenceProperty(Person)
    @classmethod
    def CreateNew(cls, code,person=None, _isAutoInsert=False):
        result = cls(
                     Person = person,
                     Code = code,
                     )
        if _isAutoInsert:
            result.put()
        return result

class HtmlImport(db.Model):
    """Imports new words into the dictionary"""
    Owner = db.ReferenceProperty(reference_class=Importer, collection_name='owner_html_imports')
    Html= db.TextProperty()
    Errors = db.TextProperty()
    DateCreated = db.DateTimeProperty(auto_now_add=True)
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Owner.Code+'('+str(self.DateCreated.year)+'-'+str(self.DateCreated.month)+'-'+str(self.DateCreated.day)+')'
    def importHtml(self, html):
        self.Html = html
        self.Owner =  Importer.gql('WHERE Code= :c',c=batchImporterCode).get() or Importer.CreateNew(code=batchImporterCode, _isAutoInsert=True)
        self.put() #Define New Importer
        from lib.BeautifulSoup import BeautifulSoup as bs
        soup = bs(html)
        wordlist = soup.findAll('b')
        result = map(lambda x: self.parseWord(x, True), wordlist)
        result = [x for x in result if x]
        self.put()
        return result
    def parseWord(self, wrd, save=True):
        try:
            value =unicode(self.unescape(wrd.getText()))
            translation =u''
            tmpNode = wrd.nextSibling 
            while tmpNode:
                translation+=tmpNode.__unicode__()
                tmpNode = tmpNode.nextSibling
            for k, v in rpl.iteritems():
                translation = translation.replace(k, v)
            translation = self.unescape(translation)
            if not value:
                self.writeError(u'Cannot Find value in'+wrd.__unicode__())
                return None
            if not translation:
                self.writeError(u'Cannot Find translation for '+value+ ' in '+wrd.__unicode__())
                return None
            result = Word.CreateNew(value, translation , self, date.today(), save)
            #self.put()
            return result
        except Exception, ex:
            logging.error(ex, ex.args)
            self.writeError(u' Error:'+ str(ex)+ex.args.__str__()+'\nValue='+(value or 'Null')+', Translation:'+(translation or 'Null'))
            return None
            #raise ex
    def writeError(self, message):
        if not self.Errors:
                self.Errors=''
        self.Errors+='\n'+message+'\n'+'*'*10+'\n'
    def unescape(self,text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError, msg:
                    self.Errors+=str(msg)
            return text # leave as is
        try:
            return re.sub("&#?\w+;", fixup, text)
        except Exception, ex:
            self.Errors+=str(ex)
class ImporterForm(ModelForm):
    class Meta():
        model=Importer
        #exclude
## End Importer
##**************************

class Word(db.Model):
    """TODO: Describe Word"""
    Value= db.StringProperty()
    Translation= db.TextProperty()
    Import = db.ReferenceProperty(reference_class=HtmlImport, collection_name='import_words')
    DateAdded= db.DateProperty(auto_now_add=True)
        
    @classmethod
    def CreateNew(cls, value, translation,wordimport,dateadded=date.today() , _isAutoInsert=False):
        value =value.replace('\r\n',' ').replace('\n', ' ')
        result = cls(
                     Value=value,
                     Translation=translation,
                     Import = wordimport,
                     DateAdded=dateadded,
                     )
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return (self.Value or 'Nu-ari Zboru')+'( '+(self.Translation or 'Nu-ari Tradutseari')+' )'
class WordForm(ModelForm):
    Value = Field(required=True)
    Translation= Field(required=True, widget=Textarea)
    class Meta():
        model=Word
        exclude = ['Import']
        #exclude
## End Word
##**************************

class Search(db.Model):
    """TODO: Describe Search"""
    text= db.StringProperty()
    
    @classmethod
    def CreateNew(cls ,text , _isAutoInsert=False):
        result = cls(
                     text=text,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
class SearchForm(ModelForm):
    class Meta():
        model=Search
        #exclude
## End Search
##**************************

