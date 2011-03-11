from google.appengine.api import users
from settings import DEBUG, OPENID_PROVIDERS
class OpenIdProviderItem(object):
    def __init__(self, url, name, imageUrl):
        self.Url = url
        self.Name = name
        self.ImageUrl = imageUrl
    @staticmethod
    def GetOpenIdProvidersList():
        result =[]
        for name,p in OPENID_PROVIDERS.iteritems():
                p_url = not DEBUG and users.create_login_url(federated_identity=p.lower()) or '/Login'
                p_image = '/images/login_icons/'+name.lower()+'.gif'
                result.append(OpenIdProviderItem(p_url, name, p_image))
        return result