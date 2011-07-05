# set models properties
from google.appengine.ext.db import Model
def cmp(self, other):
    return str(self.key()) == str(other.key())
#Easier comparison for models
setattr(Model, '__cmp__', cmp)