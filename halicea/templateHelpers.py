from halicea.config import djangoVars
def convertToTemplate(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    for k, v in input.iteritems():
        result=result.replace(v,'{-{'+k+'}-}')
    result = result.replace('{-{','{{')
    result = result.replace('}-}','}}')
    return result

def convertToReal(text,input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result=result.replace(k, v)
    for k, v in input.iteritems():
        result=result.replace(k, v)
    return result