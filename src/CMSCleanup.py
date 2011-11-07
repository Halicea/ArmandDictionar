'''
Created on Nov 7, 2011

@author: costa
'''
from google.appengine.ext import db
from Models.CMSModels import CMSLink, CMSContent, ContentTag

def flushCMS():
    #get the Contents and Links and delete them
    links = CMSLink.all(keys_only=True)
    contents = CMSContent.all(keys_only=True)
    tags = ContentTag.all(keys_only=True)
    db.delete([x for x in links]+[x for x in contents]+[x for x in tags])
