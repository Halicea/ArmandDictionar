import settings
from google.appengine.ext.db.djangoforms import ModelForm
from google.appengine.ext import db
from datetime import date
import re, htmlentitydefs
##################################################

class Word(db.Model):
    """TODO: Describe Word"""
    Value= db.StringProperty()
    Translation= db.TextProperty()
    DateAdded= db.DateProperty(auto_now_add=True)

    @classmethod
    def CreateNew(cls ,value,translation,dateadded , _isAutoInsert=False):
        result = cls(
                     Value=value,
                     Translation=translation,
                     DateAdded=dateadded,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return (self.Value or 'Nu-ari Zboru')+'( '+(self.Translation or 'Nu-ari Tradutseari')+' )'
class WordForm(ModelForm):
    class Meta():
        model=Word
        #exclude
## End Word
##**************************

class Importer(db.Model):
    """Imports new words into the dictionary"""
    Html= db.TextProperty()
    Errors = []
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method'
    def importHtml(self, html):
        from lib.BeautifulSoup import BeautifulSoup as bs
        soup = bs(html)
        wordlist = soup.findAll('b')
        result = map(lambda x: self.parseWord(x, True), wordlist) 
        return result
    def parseWord(self, wrd, save=False):
        try:
            value =self.unescape(wrd.getText())
            translation =''
            tmpNode = wrd.nextSibling 
            while tmpNode:
                translation+=str(tmpNode)
                tmpNode = tmpNode.nextSibling
            translation = self.unescape(translation)
            result = Word.CreateNew(value, translation, date.today(), save)
            return result
        except Exception, ex:
            self.Errors.append('Value='+value+', Translation:'+translation+' Error:'+ ex.message)
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
                except KeyError:
                    pass
            return text # leave as is
        try:
            return re.sub("&#?\w+;", fixup, text)
        except Exception, ex:
            self.Errors.append('Text='+text+' Error:'+ ex.message)
            return ''

class ImporterForm(ModelForm):
    class Meta():
        model=Importer
        #exclude
## End Importer
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
