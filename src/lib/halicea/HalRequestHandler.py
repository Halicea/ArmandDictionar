from google.appengine.ext import webapp
from google.appengine.ext import db
from Models.BaseModels import Person
#from lib.appengine_utilities import sessions
from lib.gaesessions import get_current_session
import lib.paths as paths
import settings
from lib.halicea.Magic import MagicSet
from os import path
import os
from google.appengine.ext.webapp import template

#from lib.webapp2 import template
 
#from lib.halicea import template

#from jinja2 import FileSystemLoader, Environment, TemplateNotFound
#from lib.halicea.jinjaCustomTags import UrlExtension
#env = Environment(loader = FileSystemLoader([settings.VIEWS_DIR,]), extensions=[UrlExtension])
from lib.NewsFeed import NewsFeed

templateGroups = {'form':settings.FORM_VIEWS_DIR, 
                  'page':settings.PAGE_VIEWS_DIR,
                  'block':settings.BLOCK_VIEWS_DIR,
                  'base':settings.BASE_VIEWS_DIR,}

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
    status = None
    isAjax=False
    op = None
    method = 'GET'
    __templateIsSet__= False
    __template__ =""
    def getTemplate(self):
        if not self.__templateIsSet__:
            self.SetTemplate(None, None, None)
        return self.__template__

    def SetTemplate(self,templateGroup=None, templateType=None, templateName=None):
        bn = MagicSet.baseName(self)
#        templateTypes = The specific modelFullName
        if not templateGroup:
            self.TemplateDir =settings.PAGE_VIEWS_DIR
        else:
            self.TemplateDir = templateGroups[templateGroup]
        if not templateType:
            self.TemplateType  = bn[:bn.rindex('.')].replace('.', path.sep)
        else:
            self.TemplateType = templateType.replace('.', path.sep)
        if not templateName: #default name will be set
            self.__template__ = os.path.join(self.TemplateDir, self.TemplateType, bn[bn.rindex('.')+1:])
            if self.op:
                self.__template__ += '_'+self.op
            self.__template__+=settings.VIEW_EXTENSTION
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
        if s and s.is_active():
            return s.get('user', default=None)
        else:
            return None
    @property
    def User(self):
        return HalRequestHandler.GetUser()

    def login_user_local(self, uname, passwd):
        self.logout_user()
        user = Person.GetUser(uname, passwd, 'local')
        if user:
            self.session['user']= user; return True            
        else:
            return False
    def login_user2(self, user):
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
        self.operations = settings.DEFAULT_OPERATIONS
    # Constructors   
    def initialize( self, request, response ):
        """Initializes this request handler with the given Request and Response."""
        self.isAjax = ((request.headers.get('HTTP_X_REQUESTED_WITH')=='XMLHttpRequest') or (request.headers.get('X-Requested-With')=='XMLHttpRequest'))
        self.request = request
        self.response = response
        self.params = RequestParameters(self.request)
        webapp.RequestHandler.__init__(self)
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
    def __route__(self, method, *args, **kwargs):
        self.method = method
        self.op = self.g('op')
        outresult = 'No Result returned'
        if self.operations.has_key(self.op):
            if isinstance(self.operations[self.op]['method'], str):
                outresult = getattr(self, self.operations[self.op]['method'])(self, *args, **kwargs)
            else:
                if hasattr(self, self.operations[self.op]['method'].__name__):
                    outresult = getattr(self, self.operations[self.op]['method'].__name__)(self, *args, **kwargs)
                else:
                    outresult = self.operations[self.op]['method'](self, *args, **kwargs)
        else:
            if isinstance(self.operations['default']['method'], str):
                outresult = getattr(self, self.operations['default']['method'])()
            else:
                if hasattr(self, self.operations['default']['method'].__name__):
                    outresult = getattr(self, self.operations['default']['method'].__name__)(self, *args, **kwargs)
                else:
                    outresult = self.operations['default']['method'](self, *args, **kwargs)
        if outresult!=None:
            self.respond(outresult)

    #otherwise we have been redirected
    def get(self, *args):
        self.__route__('GET', *args )
    def post(self, *args):
        self.__route__('POST', *args)

    def render_dict( self, basedict ):
        result = dict( basedict )
        if result.has_key( 'self' ):
            result.pop( 'self' )
        if not result.has_key( 'status' ):
            result['status'] = self.status
        if not result.has_key('current_user'):
            result['current_user'] = self.User
        if not result.has_key('current_server'):
            result['current_server']=os.environ['HTTP_HOST']
        if not result.has_key('op'):
            result['op'] = self.op
        #update the variables
        result.update(paths.GetBasesDict())
        result.update(paths.GetBlocksDict())
        result.update(paths.GetFormsDict(path.join(settings.FORM_VIEWS_DIR, self.TemplateType))) ##end
        return result

    def respond( self, item={}, *args ):
        #self.response.out.write(self.Template+'<br/>'+ dict)
        if isinstance(item, str):
            self.response.out.write(item)
        elif isinstance(item, dict):
            #commented is jinja implementation of the renderer 
            #tmpl = env.get_template(self.Template)
            #self.response.out.write(tmpl.render(self.render_dict(item)))
            self.response.out.write( template.render( self.Template, self.render_dict( item ), 
                                                  debug = settings.TEMPLATE_DEBUG ))
        elif isinstance(item,list):
            self.response.out.write('<ul>'+'\n'.join(['<li>'+str(x)+'</li>' for x in item])+'</ul>')
        elif isinstance(item,db.Model):
            self.response.out.write(item.to_xml())
        elif isinstance(item, NewsFeed):
            self.response.headers["Content-Type"] = "application/xml; charset=utf-8"
            #commented is jinja implementation of the renderer 
            #tmpl = env.get_template(os.path.join(settings.TEMPLATE_DIRS, 'RssTemplate.txt'))
            #self.response.out.write(tmpl.render({'m':item}))
            template.render(os.path.join(settings.TEMPLATE_DIRS, 'RssTemplate.txt'), 
                            {'m':item}, debug=settings.DEBUG)
        else:
            self.response.out.write(str(item))
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

