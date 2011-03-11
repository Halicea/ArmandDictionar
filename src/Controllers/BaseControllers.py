from google.appengine.api import urlfetch
from django.utils import simplejson
import urllib, os
import settings
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import ErrorSafe, LogInRequired
from Models.BaseModels import RoleAssociation, RoleAssociationForm 
from Models.BaseModels import Role, RoleForm 
from Models.BaseModels import Person

class LoginController( hrh ):
    def SetOperations(self):
        self.operations = {'default':{'method':self.login},
                           'JanrainAuth':{'method':self.JanrainAuth}}
    def login(self, *args):
        if self.request.method=='GET':
            self.login_get(*args)
        else:
            self.login_post(*args)
    @ErrorSafe()
    def JanrainAuth(self, *args):
        token = self.params.token
        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
          'format': 'json',
          'apiKey': '4a593fc2715670ab6a03b40653054858ffdc34a2',
          'token': token
          }
    
        r = urlfetch.fetch(url=url,
                           payload=urllib.urlencode(args),
                           method=urlfetch.POST,
                           headers={'Content-Type':'application/x-www-form-urlencoded'}
                           )
    
        json = simplejson.loads(r.content)
    
        if json['stat'] == 'ok':
            person = Person.gql("WHERE UserName= :u AND AuthenticationType= :auth", u=json['profile']['preferredUsername'], auth=json['profile']['providerName']).get()
            if not person:
                name = json['profile'].has_key('givenName') and json['profile']['givenName'] or ''
                surname = json['profile'].has_key('familyName') and json['profile']['name']['familyName'] or ''
                display  = json['profile'].has_key('displayName') and json['profile']['displayName'] or ''
                email  = json['profile'].has_key('email') and json['profile']['email'] or None
                photo = json['profile'].has_key('photo') and json['profile']['photo'] or None
                if not name and not surname and display:
                    arr = display.split(' ')
                    name = arr[0]; 
                    surname = len(arr)>1 and arr[1] or ''
                person = Person.CreateNew(uname=json['profile']['preferredUsername'], 
                                          name=name, 
                                          surname=surname,
                                          email = email, 
                                          password='openid',
                                          public=True, 
                                          notify=True, 
                                          authType=json['profile']['providerName'],
                                          photoUrl=photo,
                                          _autoSave=True)
                
            self.login_user2(person)
            self.status = 'Welcome '+person.UserName   
            self.redirect('/')
        else:
            self.status = 'Not Valid Login'
            self.respond()

    @ErrorSafe()
    def login_get( self, *args ):
        if not self.User:
            if self.g('redirect_url'):
                self.respond({'redirect_url':self.g('redirect_url')})
            else:
                self.respond()
        else:
            self.redirect( '/' )
            
    @ErrorSafe()
    def login_post(self , *args):
        uname = self.request.get( 'Email' )
        passwd = self.request.get( 'Password' )
        if (uname and passwd):
            if(self.login_user_local(uname, passwd)):
                if self.request.get( 'redirect_url' ):
                    self.redirect( self.request.get( 'redirect_url' ) )
                else:
                    self.redirect( '/' )
            else:
                self.status = 'Email Or Password are not correct!!'
                self.respond()
        else:
            self.status = 'Email Or Password are not correct!'
            self.respond()

class LogoutController( hrh ):
    @LogInRequired(message = '')
    def get( self, *args ):
        self.logout_user()
        self.redirect( LoginController.get_url() )

class AddUserController( hrh ):
    def get( self ):
        self.respond()
        
    def post( self ):
        self.SetTemplate(templateName='Thanks.html')
        try:
            user = Person( 
                           UserName = self.g('UserName'),
                           Email=self.g( 'Email' ),
                           Name=self.g( 'Name' ),
                           Surname=self.g( 'Surname' ),
                           Password=self.g( 'Password' ),
                           Public=self.g( 'Public' ) == 'on' and True or False,
                           Notify=self.g( 'Notify' ) == 'on' and  True or False
                           )

            if ( self.request.get( 'Notify' ) == None and self.request.get( 'Notify' ) == 'on' ):
                user.Notify = True
            else:
                user.Notify = False

            if ( self.request.get( 'Public' ) == None and self.request.get( 'Public' ) == 'on' ):
                user.Public = True
            else:
                user.Public = False
            user.put()
            self.respond( locals() )
        except Exception, ex:
            self.status = ex
            self.redirect(AddUserController.get_url())


class RoleController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def show(self):
        self.SetTemplate(templateName='Role_shw.html')
        if self.params.key:
            item = Role.get(self.params.key)
            if item:
                result = {'op':'upd', 'RoleForm': RoleForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'Role does not exists'
                self.redirect(RoleController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'RoleForm':RoleForm()})


    def delete(self):
        if self.params.key:
            item = Role.get(self.params.key)
            if item:
                item.delete()
                self.status ='Role is deleted!'
            else:
                self.status='Role does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(RoleController.get_url())


    def list(self):
        self.SetTemplate(templateName='Role_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'RoleList': Role.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)

    def insert(self):
        instance = None
        if self.params.key:
            instance = Role.get(self.params.key)
        form=RoleForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Role is saved'
            self.redirect(RoleController.get_url())
        else:
            self.SetTemplate(templateName = 'Role_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'RoleForm': form}
            self.respond(result)

class RoleAssociationController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS.copy()
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}

    def show(self, *args):   
        self.SetTemplate(templateName='RoleAssociation_shw.html')
        if self.params.key:
            item = RoleAssociation.get(self.params.key)
            if item:
                result = {'op':'upd', 'RoleAssociationForm': RoleAssociationForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'RoleAssociation does not exists'
                self.redirect(RoleAssociationController.get_url())
        else:
            self.status = 'Key not provided'
            self.respond({'op':'ins' ,'RoleAssociationForm':RoleAssociationForm()})

    def delete(self, *args):
        if self.params.key:
            item = RoleAssociation.get(self.params.key)
            if item:
                item.delete()
                self.status ='RoleAssociation is deleted!'
            else:
                self.status='RoleAssociation does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(RoleAssociationController.get_url())

    def list(self, *args):
        self.SetTemplate(templateName='RoleAssociation_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'RoleAssociationList': RoleAssociation.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)

    def insert(self, *args):
        instance = None
        if self.params.key:
            instance = RoleAssociation.get(self.params.key)
        form=RoleAssociationForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'RoleAssociation is saved'
            self.redirect(RoleAssociationController.get_url())
        else:
            self.SetTemplate(templateName = 'RoleAssociation_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'RoleAssociationForm': form}
            self.respond(result)

from Models.BaseModels import WishList, WishListForm 
class WishListController(hrh):
    def SetOperations(self):
        self.operations = settings.DEFAULT_OPERATIONS
        ##make new handlers and attach them
        #self.operations.update({'xml':{'method':'xmlCV'}})
        self.operations['default'] = {'method':'list'}
    
    def list(self):
        self.SetTemplate(templateName='WishList_lst.html')
        results =None
        index = 0; count=1000
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        result = {'WishListList': WishList.all().fetch(limit=count, offset=index)}
        result.update(locals())
        self.respond(result)


    def show(self):
        self.SetTemplate(templateName='WishList_shw.html')
        if self.params.key:
            item = WishList.get(self.params.key)
            if item:
                result = {'op':'upd', 'WishListForm': WishListForm(instance=item)}
                self.respond(result)
            else:
                self.status = 'WishList does not exists'
                self.redirect(WishListController.get_url())
        else:
            if self.method == 'POST':
                self.status = 'Key not provided'
            self.respond({'op':'ins' ,'WishListForm':WishListForm()})


    def insert(self):
        form = None
        if self.params.key:
            instance = WishList.get(self.params.key)
            form = WishListForm(instance=instance) 
        else:
            form = WishListForm(data=self.request.POST)
        if form.is_valid():
            result=form.save(commit=False)
            result.Owner = self.User
            result.put()
            self.status = 'WishList is saved'
            self.redirect(WishListController.get_url())
        else:
            self.SetTemplate(templateName = 'WishList_shw.html')
            self.status = 'Form is not Valid'
            result = {'op':'upd', 'WishListForm': form}
            self.respond(result)

    def delete(self):
        if self.params.key:
            item = WishList.get(self.params.key)
            if item:
                item.delete()
                self.status ='WishList is deleted!'
            else:
                self.status='WishList does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(WishListController.get_url())

