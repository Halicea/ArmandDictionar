import settings
from lib.HalRequestHandler import HalRequestHandler as hrh
from lib.decorators import *
from google.appengine.ext import db
##################################################
from Models.DictModels import Word, WordForm 
import os
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
                index -= count
            count = abs(count)
        except:
            pass
        result = {'WordList': Word.all().fetch(limit=count, offset=index), 'index':index, 'count':count }
        result.update(locals())
        self.respond(result)
    @AdminOnly
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
from Models.DictModels import Importer, ImporterForm 
class ImporterController(hrh):
    def SetOperations(self):
        #self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['import']={'method':'importHtml'}
        self.operations['default'] = {'method':'importHtml'}
    @AdminOnly()
    def importHtml(self,*args):
        self.SetTemplate(templateName ='Importer_import.html')
        if self.method == 'GET':
            imp = Importer()
            self.respond({'Importer':imp,})
        elif self.method=='POST' and self.params.Html:
            imp = Importer()
            imp.Html = self.params.Html
            WordList = imp.importHtml(self.params.Html)
            d = {'Importer':imp, 'WordList':WordList, 'check':True}
            self.respond(d)

from Models.DictModels import Search, SearchForm
class SearchController(hrh):
    def SetOperations(self):
        self.operations['default']={'method':'search'}
    def search(self, *args):
        offset = self.params.offset and int(self.params.offset) or 0 
        sf = SearchForm()
        results =[]
        if self.params.text:
            results = Search.gql('WHERE Value= :v', v=self.params.text).fetch(limit=100, offset=offset)
        self.respond({'SearchForm':sf,'results':results, 'offset':offset+100})
        
if __name__=='__main__':
    import pickle
    rootDir = 'DictFiles'
    f = open(sys.argv[1])
    txt=f.read()
    im= Importer()
    res = im.importHtml(txt)
    counter = 0
    for t in range(0, len(res)):
        f = open(os.path.join(rootDir, counter), 'w')
        pickle.Pickler(f)
    errorsFile = 'errors.log'
    countFile = 'count.log'
    f = open(errorsFile,'w')
        