from django.newforms import widgets, fields, extras
from google.appengine.ext.db.djangoforms import ModelForm
from Models.ChatModels import *
#{%block imports%}
#{%endblock%}
###############

class UserForm(ModelForm):
    class Meta():
        model=User
        #exclude
##End User

class RoomForm(ModelForm):
    class Meta():
        model=Room
        #exclude
##End Room

class UserInRoomForm(ModelForm):
    class Meta():
        model=UserInRoom
        #exclude
##End UserInRoom

class MessageForm(ModelForm):
    class Meta():
        model=Message
        #exclude
##End Message
