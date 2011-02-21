# -*- coding: utf-8 -*-
import settings
from google.appengine.ext.db.djangoforms import ModelForm, ModelChoiceField
from google.appengine.ext import db
from datetime import date
import re, htmlentitydefs
import logging
from BaseModels import Person
from django.newforms.fields import ChoiceField, EmailField, Field
from django.newforms.widgets import RadioSelect, Textarea, TextInput
from django.newforms import widgets, fields, extras
import BaseModels
from django import forms
va =u'ã'
rpl ={u'â':va, u'Ã£':va, u'ã':va}

batchImporterCode = 'Batch'
class Language(db.Model):
    """TODO: Describe Language"""
    Code = db.StringProperty(required=True, )
    Name= db.StringProperty(required=True, )
    DateAdded= db.DateProperty(auto_now_add=True, )
    AddedBy= db.ReferenceProperty(BaseModels.Person, collection_name='addedby_languages', )
    TotalWordCount= db.IntegerProperty(default=0, )
    
    @classmethod
    def CreateNew(cls ,name,dateadded,addedby,totalwordcount , _isAutoInsert=False):
        result = cls(
                     Name=name,
                     DateAdded=dateadded,
                     AddedBy=addedby,
                     TotalWordCount=totalwordcount,)
        if _isAutoInsert: result.put()
        return result
    @classmethod
    def GetByCode(cls, code):
        return Language.gql('WHERE Code= :c', c=code).get()
    @classmethod
    def GetByName(cls, name):
        return Language.gql('WHERE Name= :n', n=name).get()
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Name
class LanguageForm(ModelForm):
    class Meta():
        model=Language
        #exclude
## End Language
##**************************

class Dictionary(db.Model):
    """TODO: Describe Dictionary"""
    Name= db.StringProperty()
    AddedBy= db.ReferenceProperty(BaseModels.Person, collection_name='addedby_dictionarys', required=True, )
    DateAdded= db.DateProperty(auto_now_add=True, )
    Language1= db.ReferenceProperty(Language, collection_name='language1_dictionarys', required=True, )
    Language2= db.ReferenceProperty(Language, collection_name='language2_dictionarys', required=True, )
    WordCount= db.IntegerProperty(default=0, )
    
    @classmethod
    def CreateNew(cls ,name,addedby,dateadded,language1,language2,wordcount , _isAutoInsert=False):
        result = cls(
                     Name=name,
                     AddedBy=addedby,
                     DateAdded=dateadded,
                     Language1=language1,
                     Language2=language2,
                     WordCount=wordcount,)
        if _isAutoInsert: result.put()
        return result
    
    def GetTranslations(self, word):
        return self.dictionary_words.limit('Value=', word).fetch(limit=100)
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Name+'('+self.Language1.Name+'-'+(self.Language2==None and 'None' or self.Language2.Name)+')'

class DictionaryForm(ModelForm):
    DateAdded= fields.DateField(widget=TextInput(attrs={'class':'date'}))
    class Meta():
        model=Dictionary
        #exclude
## End Dictionary
##**************************

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
    Dictionary = db.ReferenceProperty(Dictionary, collection_name='dictionary_html_imports')
    def __str__(self):
        return self.Owner.Code+'('+str(self.DateCreated.year)+'-'+str(self.DateCreated.month)+'-'+str(self.DateCreated.day)+')'
    def importWord(self, word):
        word.Import = self
        word.put() 
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
    Dictionary = db.ReferenceProperty(reference_class=Dictionary, collection_name='dictionary_words')
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
    def put(self):
        if not self.is_saved():
#           increment the Counters for each saved word
            self.Dictionary.WordCount+=1
            self.Dictionary.Language1.TotalWordCount+=1
            self.Dictionary.put()
            self.Dictionary.Language1.put()
            self.put()
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return (self.Value or 'Nu-ari Zboru')+'( '+(self.Translation or 'Nu-ari Tradutseari')+' )'
class WordForm(ModelForm):
    Value = Field(required=True)
#    Translation= Field(required=True, widget=Textarea)
#    res= (HalRequestHandler.GetUser()==None and [[]] or [HalRequestHandler.GetUser().addedby_dictionarys])[0]
#    Dictionary = ModelChoiceField(Dictionary, required=True, widget=widgets.Select)
    class Meta():
        model=Word
        exclude = ['Import']
        #exclude
## End Word
##**************************

class Search(db.Model):
    """TODO: Describe Search"""
    Text= db.StringProperty()
    Language1 = db.ReferenceProperty(Language, collection_name='language1_searches')
    Language2 = db.ReferenceProperty(Language, collection_name='language2_searches')
    @classmethod
    def CreateNew(cls ,text ,language1, language2, _isAutoInsert=False):
        result = cls(
                     Text=text,
                     Language1=language1,
                     Language2=language2,
                     )
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return self.Text+'-'+self.Language 
class SearchForm(ModelForm):
    Text = Field(widget=widgets.TextInput, label='Збор')
    Language1 = ModelChoiceField(Language, label="", widget= fields.HiddenInput,)
    Language2 = ModelChoiceField(Language, label="", widget= fields.HiddenInput,)
    class Meta():
        model=Search
        #exclude
## End Search
##**************************

class WordSugestion(db.Model):
    """TODO: Describe WordSugestion"""
    Word= db.ReferenceProperty(Word, collection_name='word_wordsugestions', required=True, )
    Sugestion= db.TextProperty()
    SugestedBy= db.ReferenceProperty(Person, collection_name='sugestedby_wordsugestions', required=True, )
    DateCreated= db.DateProperty()
    
    @classmethod
    def CreateNew(cls ,word,sugestion,sugestedby , _isAutoInsert=False):
        result = cls(
                     Word=word,
                     Sugestion=sugestion,
                     SugestedBy=sugestedby,
                     DateCreated=date.to,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method'
class WordSugestionForm(ModelForm):
    class Meta():
        model=WordSugestion
        #exclude
## End WordSugestion
##**************************
