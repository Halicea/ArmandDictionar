from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from google.appengine.api import memcache
from lib.ArmanDict import MunicipalityList
from lib.ascii2cyrillic import replaceWithCyrillic
from django.utils import simplejson
class GetMunicipality(hrh):
    def SetDefaultOperations(self):
        self.operations = {'default':{'method':self.search}}
    def search(self, query):
        q = replaceWithCyrillic(query)
        results = [x for x in MunicipalityList if x.startswith(q)]
        return results