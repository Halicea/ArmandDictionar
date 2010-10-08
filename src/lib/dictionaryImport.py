'''
Created on Oct 6, 2010

@author: KMihajlov
'''
import pickle
import os
import codecs
import urllib
error_log = open(os.path.join('Errors', 'errors.log'), 'w')
error_counter = 0
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
#    urllib
#    urlopen('http://localhost:8080/Dict/Importer')
if __name__ == '__main__':
    urlLive = 'http://armandict.appspot.com/Dict/Importer'
    urlLocal = 'http://localhost:8080/Dict/Importer'
    bulkDelete(urlLocal)
    bulkImport(1, 1386, urlLocal)