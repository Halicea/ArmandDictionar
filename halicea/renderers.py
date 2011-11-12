from django import template

from django.template.loader import *
class HalTemplate(object):
    def __init__(self, text):
        self.text = text
    def render(self, context):
        raise NotImplementedError('This class needs to be inherited')

class Django(HalTemplate):
    def __init__(self, text):
        HalTemplate.__init__(self, text)
        self.template = template.Template(text)
    def render(self, dict):
        return self.template.render(template.Context(dict))

