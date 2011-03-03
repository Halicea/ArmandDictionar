import settings
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *
from google.appengine.ext import db
#{%block imports%}
from Models.ChatModels import User
from Forms.ChatForms import UserForm
from Models.ChatModels import Room
from Forms.ChatForms import RoomForm
from Models.ChatModels import UserInRoom
from Forms.ChatForms import UserInRoomForm
from Models.ChatModels import Message
from Forms.ChatForms import MessageForm
#{%endblock%}
################################

class UserController(hrh):
    
    def edit(self, *args):
        self.SetTemplate(templateName='User_edit.html')
        if self.params.key:
            item = User.get(self.params.key)
            if item:
                return {'op':'update', 'UserForm': UserForm(instance=item)}
            else:
                self.status = 'User does not exists'
                self.redirect(UserController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'UserForm':UserForm()}

    def details(self, *args):
        self.SetTemplate(templateName='User_details.html')
        if self.params.key:
            item = User.get(self.params.key)
            if item:
                return {'op':'upd', 'UserForm': UserForm(instance=item)}
            else:
                self.status = 'User does not exists'
                self.redirect(UserController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'ins' ,'UserForm':UserForm()}

    def delete(self,*args):
        if self.params.key:
            item = User.get(self.params.key)
            if item:
                item.delete()
                self.status ='User is deleted!'
            else:
                self.status='User does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(UserController.get_url())

    def save(self, *args):
        instance = None
        if self.params.key:
            instance = User.get(self.params.key)
        form=UserForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'User is saved'
            self.redirect(UserController.get_url())
        else:
            self.SetTemplate(templateName = 'User_shw.html')
            self.status = 'Form is not Valid'
            return {'op':'upd', 'UserForm': form}

    def index(self, *args):
        self.SetTemplate(templateName="User_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'UserList': User.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

class RoomController(hrh):
    
    def edit(self, *args):
        self.SetTemplate(templateName='Room_edit.html')
        if self.params.key:
            item = Room.get(self.params.key)
            if item:
                return {'op':'update', 'RoomForm': RoomForm(instance=item)}
            else:
                self.status = 'Room does not exists'
                self.redirect(RoomController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'RoomForm':RoomForm()}

    def details(self, *args):
        self.SetTemplate(templateName='Room_details.html')
        if self.params.key:
            item = Room.get(self.params.key)
            if item:
                return {'op':'upd', 'RoomForm': RoomForm(instance=item)}
            else:
                self.status = 'Room does not exists'
                self.redirect(RoomController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'ins' ,'RoomForm':RoomForm()}

    def delete(self,*args):
        if self.params.key:
            item = Room.get(self.params.key)
            if item:
                item.delete()
                self.status ='Room is deleted!'
            else:
                self.status='Room does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(RoomController.get_url())

    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Room.get(self.params.key)
        form=RoomForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Room is saved'
            self.redirect(RoomController.get_url())
        else:
            self.SetTemplate(templateName = 'Room_shw.html')
            self.status = 'Form is not Valid'
            return {'op':'upd', 'RoomForm': form}

    def index(self, *args):
        self.SetTemplate(templateName="Room_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'RoomList': Room.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

class UserInRoomController(hrh):
    def edit(self, *args):
        self.SetTemplate(templateName='UserInRoom_edit.html')
        if self.params.key:
            item = UserInRoom.get(self.params.key)
            if item:
                return {'op':'update', 'UserInRoomForm': UserInRoomForm(instance=item)}
            else:
                self.status = 'UserInRoom does not exists'
                self.redirect(UserInRoomController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'UserInRoomForm':UserInRoomForm()}

    def details(self, *args):
        self.SetTemplate(templateName='UserInRoom_details.html')
        if self.params.key:
            item = UserInRoom.get(self.params.key)
            if item:
                return {'op':'upd', 'UserInRoomForm': UserInRoomForm(instance=item)}
            else:
                self.status = 'UserInRoom does not exists'
                self.redirect(UserInRoomController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'ins' ,'UserInRoomForm':UserInRoomForm()}

    def delete(self,*args):
        if self.params.key:
            item = UserInRoom.get(self.params.key)
            if item:
                item.delete()
                self.status ='UserInRoom is deleted!'
            else:
                self.status='UserInRoom does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(UserInRoomController.get_url())

    def save(self, *args):
        instance = None
        if self.params.key:
            instance = UserInRoom.get(self.params.key)
        form=UserInRoomForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'UserInRoom is saved'
            self.redirect(UserInRoomController.get_url())
        else:
            self.SetTemplate(templateName = 'UserInRoom_shw.html')
            self.status = 'Form is not Valid'
            return {'op':'upd', 'UserInRoomForm': form}

    def index(self, *args):
        self.SetTemplate(templateName="UserInRoom_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'UserInRoomList': UserInRoom.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result

class MessageController(hrh):
    
    def edit(self, *args):
        self.SetTemplate(templateName='Message_edit.html')
        if self.params.key:
            item = Message.get(self.params.key)
            if item:
                return {'op':'update', 'MessageForm': MessageForm(instance=item)}
            else:
                self.status = 'Message does not exists'
                self.redirect(MessageController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'insert' ,'MessageForm':MessageForm()}

    def details(self, *args):
        self.SetTemplate(templateName='Message_details.html')
        if self.params.key:
            item = Message.get(self.params.key)
            if item:
                return {'op':'upd', 'MessageForm': MessageForm(instance=item)}
            else:
                self.status = 'Message does not exists'
                self.redirect(MessageController.get_url())
        else:
            self.status = 'Key not provided'
            return {'op':'ins' ,'MessageForm':MessageForm()}

    def delete(self,*args):
        if self.params.key:
            item = Message.get(self.params.key)
            if item:
                item.delete()
                self.status ='Message is deleted!'
            else:
                self.status='Message does not exist'
        else:
            self.status = 'Key was not Provided!'
        self.redirect(MessageController.get_url())

    def save(self, *args):
        instance = None
        if self.params.key:
            instance = Message.get(self.params.key)
        form=MessageForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            result=form.save(commit=False)
            result.put()
            self.status = 'Message is saved'
            self.redirect(MessageController.get_url())
        else:
            self.SetTemplate(templateName = 'Message_shw.html')
            self.status = 'Form is not Valid'
            return {'op':'upd', 'MessageForm': form}

    def index(self, *args):
        self.SetTemplate(templateName="Message_index.html")
        results =None
        index = 0; count=20
        try:
            index = int(self.params.index)
            count = int(self.params.count)
        except:
            pass
        nextIndex = index+count;
        previousIndex = index<=0 and -1 or (index-count>0 and 0 or index-count) 
        result = {'MessageList': Message.all().fetch(limit=count, offset=index)}
        result.update(locals())
        return result
