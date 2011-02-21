from string import Template

class BlockLocator(object):
    blockTemplate = None
    def lineIsBlockBegin(self):
        pass
    def lineIsBlockEnd(self):
        pass
    def createValidBlock(self, blockname, content=[], blIndent=0, indent=0):
        if not self.blockTemplate:
            raise NotImplementedError('Block Template was not provided')
        result = Template(self.blockTemplate).substitute(blindent=' '*blIndent, blockname=blockname)
        if not content:
            return result.replace('#content#\n','')
        else:
            return result.replace('#content#','\n'.join([(' '*indent)+line for line in content]))

class GenericCbl(BlockLocator):
    def __init__(self, blockBeginLocator, blockEndLocator, blockTemplate=None):
        self.blockTemplate = blockTemplate
        self.lineIsBlockBegin = blockBeginLocator
        self.lineIsBlockEnd = blockEndLocator

class HalCodeBlockLocator(BlockLocator):
    blockTemplate = '''$blindent{%block $blockname%}
#content#
$blindent{%endblock%}
'''
    def lineIsBlockBegin(self, line):
        if line.replace(' ','').find('{%block')>=0 and line.replace(' ','').find('%}')>0:
            return strBetween(line.replace(' ',''), '{%block', '%}')
        else: 
            return None
    def lineIsBlockEnd(self, line):
        return line.replace(' ','').find('{%endblock%}')>=0

class InPythonBlockLocator(BlockLocator):
    blockTemplate = \
'''$blindent#{%block $blockname%}
#content#
$blindent#{%endblock%}
'''
    def lineIsBlockBegin(self, line):
        if line.replace(' ','').find('#{%block')>=0 and line.replace(' ','').find('%}')>0:
            return strBetween(line.replace(' ',''), '#{%block', '%}')
        else: 
            return None
    def lineIsBlockEnd(self, line):
        return line.replace(' ','').find('#{%endblock%}')>=0

def strBetween(line, strLeft, strRigth, strip=True ):
    fromIndex=line.index(strLeft)+len(strLeft)
    toIndex = fromIndex+line[fromIndex:].index(strRigth)
    result = line[fromIndex:toIndex]
    if strip: 
        return result.strip()
    else: 
        return result
