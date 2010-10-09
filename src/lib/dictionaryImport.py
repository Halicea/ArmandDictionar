'''
Created on Oct 6, 2010

@author: KMihajlov
'''
import pdb
import pickle
import os
import codecs
import urllib
from BeautifulSoup import BeautifulSoup as bs
import sys
sourcesDir = 'DictFiles2'
import time
retryTimes = 1
chunkSize = 100
def bulkDelete(url):
    old = 100
    negatives =0
    k = 0
    for t in range(0, 25000):
        try:
            prs = urllib.urlencode({'op':'bulkDelete','From':str(k)})
            respond = urllib.urlopen(url, prs)    
            if negatives>=2*retryTimes:
                print str(2*retryTimes),' negatives in a row, closing'
                return
            k = respond.read()
            time.sleep(1)
            try:
                k = int(k)
                if k>0:
                    negatives = 0
                    print 'deleted', str(old)
                else:
                    if negatives==retryTimes:
                        k=old+100
                        print 'tried', str(retryTimes), 'times for', str(old), 'going to next 100' 
                    else:
                        k=old
                    negatives+=1
                    print 'Got Negative for '+str(old)
                old = k
            except Exception, msg:
                print msg
                negatives+=1
                k = old+100
            respond.close()
        except Exception, msg:
            print k, old, negatives
            print msg
def bulkImport(frm, to, url):
    error_log = open('errors.log','w')
    error_counter = 0
    for t in range(frm, to):
	
        try:
            if os.path.exists(os.path.join(sourcesDir, str(t))):
                f = open(os.path.join(sourcesDir, str(t)), 'r')
                txt = f.read()
                f.close()
                #url ='http://localhost:8080/Dict/Importer'

                prs = urllib.urlencode({'op':'importHtml','Html':txt})
                respond = urllib.urlopen(url, prs)
                try:
                    stat = open(os.path.join('ErrorsPublish', str(t)+'.html'), 'w')
                    response = respond.read()
                    print response
                    stat.write(response)
                    respond.close()
                    stat.close()
                except Exception, ex:
                    respond.close()
                    error_counter+=1
                    error_log.write('\n'+str(error_counter)+'.'+ex.message)
        except Exception, ex:
            error_counter+=1
            error_log.write('\n'+str(error_counter)+'.'+ex.message)
templ = """<html>
<head></head>
<body>{{repl}}</body>
</html>"""
items = []
chunkNum =30
dumpDir = '../../Docs/ResultFiles2'
resourceFile ='../../Docs/MakGood.htm'
def chunkHtml():
    f = open(resourceFile, 'r')
    txt =f.read()
    f.close()
    soup  = bs(txt)
    items = soup.findAll('b')
    counter = 1
    if not os.path.exists(dumpDir):
        os.makedirs(dumpDir)
    for t in range(0, len(items), chunkNum):
        to = len(items)>t+chunkNum and t+chunkNum or len(items)-t
        print t, to, len(items)
        c = items[t:to]
        result= ''
        for ut in c:
            res = str(ut)
            tmpNode = ut.nextSibling
            while tmpNode:
                res+=str(tmpNode)
                tmpNode = tmpNode.nextSibling
            final = '\n<div>'+res+'</div>\n'
            result+=final
        result = templ.replace('{{repl}}', result)
        f = open(os.path.join(dumpDir, str(counter)), 'w')
	f.write(result)
        f.close()
	print 'saved '+str(counter)+' to '+dumpDir
        counter+=1
	    
#    urlopen('http://localhost:8080/Dict/Importer')
if __name__ == '__main__':
#    pdb.set_trace()
    urlLive = 'http://armandict.appspot.com/Dict/Importer'
    urlLocal = 'http://localhost:8080/Dict/Importer'
    url= urlLocal
    if len(sys.argv)>2:
        if sys.argv[2]=='live':
            url = urlLive
    if len(sys.argv) > 1:
        if sys.argv[1] == 'chunk':
            chunkHtml()
        elif sys.argv[1] =='del':
            bulkDelete(url)
        elif sys.argv[1] == 'import':
            bulkImport(1, 1386, url)
        else:
            bulkDelete(url)
            print 'no argument passed'



