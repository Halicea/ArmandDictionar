# -*- coding: utf-8 -*-
#{% block imports %}
import settings
from lib.HalRequestHandler import HalRequestHandler as hrh
from lib.decorators import *
from google.appengine.ext import db
from google.appengine.runtime import apiproxy_errors

from lib.ascii2cyrillic import asciiToCyrillic as a2c
from lib.ascii2cyrillic import multiAsciiToCyrillic as ma2c 
import logging
#{% endblock}

from Models.DictModels import Word, WordForm , HtmlImport
import os
import sys
from google.appengine.api.datastore_errors import TransactionFailedError
class WordController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def show(self, *args):
        self.SetTemplate(templateName='Word_shw.html')
        if self.params.key:
            item = Word.get(self.params.key)
            if item:
                result = {'op':'upd', 'WordForm': WordForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Word does not exists'
                self.redirect(WordController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'WordForm':WordForm()})

    @AdminOnly()
    def delete(self, *args):
        if self.params.key:
            item = Word.get(self.params.key)
            if item:
                item.delete()
                self.status ='Word is deleted!'
            else:
                self.status='Word does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(WordController.get_url())

    @AdminOnly()
    def list(self, *args):
        self.SetTemplate(templateName='Word_lst.html')
        results =None
        index = 0; count=50
        try:
            index = int(self.params.index)
            count = int(self.params.count)
            if count<0:
                index += count
        except:
            pass
        r= Word.all().fetch(limit=abs(count), offset=index)
        index+=count
        result = {'WordList':r, 'index':index, 'count':abs(count) }
        self.respond(result)
    @AdminOnly()
    def insert(self, *args):
        instance = None
        if self.params.key:
            instance = Word.get(self.params.key)
        form=WordForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.Value = result.Value.replace('<p>', '').replace('</p>', '')
#            result.Translation = result.Translation.strip('<p>') 
            result.put()
            self.status = 'Word is saved'
            self.redirect(WordController.get_url())
        else:
            self.SetTemplate(templateName = 'Word_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'WordForm': form}
            self.respond(result)

from Models.DictModels import Search, SearchForm
class SearchController(hrh):
    def SetOperations(self):
        self.operations['default']={'method':'search'}
    def search(self, *args):
        offset = self.params.offset and int(self.params.offset) or 0 
        sf = SearchForm(self.request.POST)
        results =[]
        showMessage=False
        if self.params.text:
            showMessage=True
            val = self.params.text
            for k, v in ma2c.iteritems():
                val = val.replace(k, v)
            for k, v in a2c.iteritems():
                val = val.replace(k, v)
            results = Word.gql('WHERE Value= :v', v=val).fetch(limit=100, offset=offset)
        self.respond({'SearchForm':sf,'results':results, 'offset':offset+100, 'showMessage':showMessage})

from Models.DictModels import Importer, ImporterForm 
import pickle
import time
class ImporterController(hrh):
    def SetOperations(self):
        #self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['import']={'method':'importHtml'}
        self.operations['default'] = {'method':'importHtml'}
        self.operations['importPickle'] = {'method':'importPickle'}
        self.operations['bulkDelete']={'method':'bulkDelete'}
    #@AdminOnly()
    def bulkDelete(self, *args):
        try:
            f=int(self.params.From)
            items = Word.all().fetch(limit=100, offset=0)
            if len(items)>0:
                db.delete(items)
                self.response.out.write(str(f+100))
            else:
                self.response.out.write('-1')
            time.sleep(0.5)
        except TransactionFailedError, msg:
            logging.error(msg)
            self.response.out.write('-1')
        except Exception, msg:
            logging.error(msg)
            self.response.out.write('-1')
    def importHtml(self,*args):
        try:
            self.SetTemplate(templateName ='Importer_import.html')
            if self.method=='POST' and self.params.Html:
                imp = HtmlImport()
                imp.Html = self.params.Html
#                pdb.set_trace()
                WordList = imp.importHtml(self.params.Html)
                #d = {'Importer':imp, 'WordList':WordList, 'check':True}
                self.response.out.write(len(WordList))
        except Exception, ex:
            logging.error(ex, ex.args)
    def importPickle(self, *args):
        a = pickle.loads(self.params.pck)
        cnt = 0
        err= 0
        for t in a:
            try:
                word = Word.CreateNew(value=t.Value, translation=t.Translation, _isAutoInsert=True)
                cnt+=1
            except:
                err+=1
                pass
        self.response.out.write(str(cnt)+'---'+err.message)