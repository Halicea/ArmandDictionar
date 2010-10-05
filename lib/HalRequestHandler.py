'''
Created on Aug 6, 2009
@author: kosta
'''

from google.appengine.ext import webapp
from Models.BaseModels import Person
#from lib.appengine_utilities import sessions
from lib.gaesessions import get_current_session
import lib.paths as paths

import settings
from os import path
import os
from google.appengine.ext.webapp import template

__mode__ = 'Debug'


class RequestParameters(object):
    def __init__(self, request):
        self.request = request
    def __getattr__(self, name):
        return self.request.get(name)
    
class HalRequestHandler( webapp.RequestHandler ):
    params = None
    operations = {}
    TemplateDir = settings.PAGE_VIEWS_DIR
    TemplateType = ''
    quote = None
    status = None
    isAjax=False
    op = None
    method = 'GET'
    __templateIsSet__= False
    __template__ =""
    def getTemplate(self):
        if not self.__templateIsSet__:
            self.SetTemplate(None, None)
        return self.__template__

    def SetTemplate(self, templateType=None, templateName=None):
        if not templateType:
            self.TemplateType = self.__class__.__module__[self.__class__.__module__.index('.')+1:]
            self.TemplateType = self.TemplateType[:self.TemplateType.rindex('Controllers')]
        else:
            self.TemplateType = templateType.replace('.', path.sep)
            
        if not templateName: #default name will be set
            self.__template__ = self.__class__.__name__
            self.__template__ = self.__template__[:self.__template__.rindex('Controller')]+".html"
            self.__template__ = os.path.join(self.TemplateDir, self.TemplateType, self.__template__)
        else:
            self.__template__ = os.path.join(self.TemplateDir, self.TemplateType, templateName)
        self.__templateIsSet__ = True

    Template =property(getTemplate)
    def __getSession__(self):
        return get_current_session()
    session = property(__getSession__)

    @classmethod
    def GetUser(cls):
        s = get_current_session()
        if s.is_active():
            return s.get('user', default=None)
        else:
            return None
    @property
    def User(self):
        return HalRequestHandler.GetUser()

    def login_user(self, uname, passwd):
        self.logout_user()
        user = Person.GetUser(uname, passwd)
        if user:
            self.session['user']= user; return True            
        else:
            return False
    def logout_user(self):
        if self.session.is_active():
            self.session.terminate()
        return True
    #request =None
    # end Properties
    def SetOperations(self):
        pass
    
    # Constructors   
    def initialize( self, request, response ):
        """Initializes this request handler with the given Request and Response."""
        self.isAjax = ((request.headers.get('HTTP_X_REQUESTED_WITH')=='XMLHttpRequest') or (request.headers.get('X-Requested-With')=='XMLHttpRequest'))
        self.request = request
        self.response = response
        webapp.RequestHandler.__init__( self )
        #self.request = super(MyRequestHandler, self).request
        if not self.isAjax: self.isAjax = self.g('isAjax')=='true'
        # set the status variable
        if self.session.has_key( 'status' ):
            self.status = self.session.pop('status')
        self.operations = {}
        self.SetOperations()
# Methods
    def g(self, item):
        return self.request.get(item)

#   the method by the operation
    def __route__(self, method, *args):
        self.method = method
        self.params = RequestParameters(self.request)
        
        self.op = self.g('op')
        if self.op in self.operations.iterkeys():
            getattr(self, self.operations[self.op]['method'])()
        else:
            getattr(self, self.operations['default']['method'])()

    def get(self, *args):
        self.__route__('GET')

    def post(self, *args):
        self.__route__('POST')
        
    def render_dict( self, basedict ):
        result = dict( basedict )
        if result.has_key( 'self' ):
            result.pop( 'self' )
        if not result.has_key( 'status' ):
            result['status'] = self.status
        if not result.has_key( 'quote' ):
            result['quote'] = self.quote
        if not result.has_key( 'mode' ):
            result['mode'] = __mode__
        if not result.has_key('current_user'):
            result['current_user'] = self.User
        if not result.has_key('op'):
            result['op'] = self.op
        #update the variables about the references
        result.update(paths.GetBasesDict())
        result.update(paths.GetMenusDict())
        result.update(paths.GetBlocksDict())
        result.update(paths.getViewsDict(path.join(settings.FORM_VIEWS_DIR, self.TemplateType)))        ##end
        return result
    def respond( self, dict={} ):
        #self.response.out.write(self.Template+'<br/>'+ dict)
        self.response.out.write( template.render( self.Template, self.render_dict( dict ), 
                                                  debug = settings.TEMPLATE_DEBUG ) )
    def redirect_login( self ):
        self.redirect( '/Login' )
    def respond_static(self, text):
        self.response.out.write(text)    
    def redirect( self, uri, postargs={}, permanent=False ):
        innerdict = dict( postargs )
        if innerdict.has_key( 'status' ):
            self.status = innerdict['status']
            del innerdict['status']
        if self.status:
            self.session['status']=self.status
        if uri=='/Login' and not self.request.url.endswith('/Logout'):
            innerdict['redirect_url']=self.request.url
        if innerdict and len( innerdict ) > 0:
            params= '&'.join( [k + '=' + str(innerdict[k]) for k in innerdict] )
            if uri.find('?')==-1:
                webapp.RequestHandler.redirect( self, uri + '?' + params, permanent )
            elif uri.endswith('&'):
                webapp.RequestHandler.redirect( self, uri + params, permanent )
            else:
                webapp.RequestHandler.redirect( self, uri+ '&' + params, permanent )
        else:
            webapp.RequestHandler.redirect( self, uri, permanent )

