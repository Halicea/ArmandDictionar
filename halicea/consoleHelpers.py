def extractAgrs(paramsList):
    return dict(map(lambda x:(x[:x.index('=')], x[x.index('=')+1:]), paramsList))

def ask(message, validOptions={'y':True,'n':False}):
    yesno =''
    if isinstance(validOptions, str):
        #print validOptions
        yesno = raw_input(message)
    else:
        #print validOptions.keys()
        yesno = raw_input(message+'('+'/'.join(validOptions.keys())+'):')
    while True:
        if validOptions=='*':
            return yesno
        if len(yesno)>0: 
            if validOptions.has_key(yesno):
                return validOptions[yesno]
        print 'Not Valid Input'
        yesno = raw_input(message+'('+'/'.join(validOptions.keys())+'):')
