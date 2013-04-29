# -*- coding: utf-8 -*-
import codecs
import re
import os
langs = ['ro', 'en', 'fr']
err_count = 0
tr_not_found = {'ro':0, 'en':0, 'fr':0}
with_ref=0
def parse_line(l, index):
  global err_count
  global tr_not_found
  global with_ref
  results = []
  #synonims or similar meaning
  words = l.split(u'§')
  for i in range(0, len(words)):
    res = {}
    index = 0
    w = words[i].strip()
    if ' ' in w:
      res['rmn']=w[:w.index(' ')]
      index = w.index(' ')+1
    #find translations
    for lang in langs:
      key = '{%s:'%lang
      if( key in w):
        lindex = w.index(key)+len(lang)+2
        try:
          rindex = w.index('}', lindex)
          res[lang] = w[lindex:rindex].split(',')
        except:
          err_count+=1
          #print w.encode('utf-8', errors='ignore')
      elif not ('vedz' in w):
        tr_not_found[lang] +=1
        res[lang]=[]
    if 'vedz' in w:
        with_ref+=1
        res['referece']= w[w.index('vedz')+4:]
    res['raw'] = w
    res['index'] = index
    results.append(res)
  return results

directory = '/Users/kostamihajlov/Desktop/cunia'
d =[]
merge_count = 0
warn_merge = 0
max_merge =10
current_let = None
line = 0
lines = tuple(codecs.open(os.path.join(directory,'cunia.txt'),'r', 'utf16'))
lang_matcher = "\{[fr: en: ro:].*\}"
merge_required = [u'unã cu', u'vedz', u'tu-aestu', '{ro:','{en:','{fr:']
merge_required_count = 0

for k in lines:
  clean= k.strip().replace(u'\ufffc', '')
  if len(clean)==1:
    current_let = clean
    print 'Starting with letter:%s'%current_let
  elif not clean:
    pass
  elif u"Dictsiunar a Limbãljei Armãneascã" in clean:
    pass
  else:
    merged = False
    if d:
      for k in merge_required:
        if(d[-1].endswith(k)):
          d[-1] = d[-1]+' '+clean
          merged = True
          merge_required_count+=1
          break;
    if not merged:
      if(clean[0].lower()==current_let.lower()):
        d.append(clean)
        merge_count = 0
      else:
        d[-1] = d[-1]+' '+clean
        merge_count+=1
        #print u'Merging line %s and merge count is %s'%(line, merge_count)
        if merge_count>=max_merge:
          #print 'Max Merge received on line %s'%line
          pass
  line+=1
wc = 0
final = []
index = 0
for w in d:
  final.extend(parse_line(w, index))
  index+=1

current_letter = None
prev_letter = None
f = None
for w in final:
  try:
    current_letter = w['rmn'][0]
    if current_letter!=prev_letter:
      prev_letter = current_letter
      if f: f.close()
      f = codecs.open(os.path.join(directory, current_letter+'.txt'), 'w', 'utf-16')
    f.write('%s %s en:%s fr:%s ro:%s\n'%(w['index'], w['rmn'], w['en'], w['fr'], w['ro']))
  except:
    print w

print 'Regular Merges:', merge_required_count    
print 'Total Words', len(final)
print 'Total Lines', len(d)
print 'Errors', err_count
print 'References', with_ref
print 'Without translations', tr_not_found