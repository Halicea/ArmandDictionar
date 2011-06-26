__author__ = 'KMihajlov'
from django.template.loader import BaseLoader
from settings import VIEWS_DIR
import os
class HalLoader(BaseLoader):
    def __init__(self, *args, **kwargs):
        self.is_usable = True
        
    def load_template_source(self, template_name, template_dirs=None):
        import warnings
        #TODO: implement caching
        if template_name.find(os.sep)>0:
            if os.path.exists(template_name):
                return open(template_name, 'r').read(), template_name
            else:
                raise Exception('Template '+template_name+' was not found and was given by absolute path')
        for root, dirs, files in os.walk(VIEWS_DIR):
            for f in files:
                if f == template_name:
                    warnings.warn('template '+template_name+' was found in '+root)
                    return open(os.path.join(root, f), 'r').read(), f
        raise Exception('Template '+template_name+' was not found')
