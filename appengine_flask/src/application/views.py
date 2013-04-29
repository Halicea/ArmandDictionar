import os
import logging
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect
from flask_cache import Cache

from application import app
from decorators import login_required, admin_required

from google.appengine.api import rdbms
from google.appengine.api import rdbms_mysqldb
CLOUDSQL_INSTANCE = 'halicea.com:dictdb:armandict'
LOCAL_INSTANCE = '127.0.0.1'
DATABASE_NAME = 'arman_dictionar'
USER_NAME = 'dictuser'
PASSWORD = 'dict$123'
match_col = {"mkd":"windex", "rmn":"translation"}


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def get_connection():
  #logging.info('Environment %s'%os.getenv('SETTINGS_MODE'))
  # if (os.getenv('SETTINGS_MODE') == 'prod'): # This is for production (GAE)
  return rdbms.connect(instance=CLOUDSQL_INSTANCE, database=DATABASE_NAME, user=USER_NAME, password=PASSWORD, charset="utf8")
  # else: # This is for local development
  #   rdbms_mysqldb.SetConnectKwargs(host=LOCAL_INSTANCE, port=3306,user=USER_NAME, passwd=PASSWORD)
  #   conn = rdbms.connect(instance='MySQL55', db=DATABASE_NAME, charset='utf8')

  # return rdbms.connect(instance=LOCAL_INSTANCE,database=DATABASE_NAME, user=USER_NAME, password=PASSWORD, charset="utf8")

def index():
  return render_template("index.jinja2", active='index')

def search():
  results = []
  key = "mkd"
  if request.args.get("from_lang"):
    key_n = request.args.get("from_lang")
    if key_n in match_col:
      key =key_n

  s_pat= request.args.get("Search")
  words = s_pat.split(' ')
  if len(words)>5:
    words = words[:5]

  for word in words:
    conn = get_connection()
    cursor = conn.cursor()
    q_long=u"SELECT * FROM word WHERE MATCH(%s) AGAINST ('%s')"%(match_col[key], word)
    q_short = u"SELECT * FROM word where windex like '%(search)s %%' or windex like '%% %(search)s ' or windex like '%% %(search)s'"%{"search":word}
    if len(word)>3:
      cursor.execute(q_long)
    else:
      cursor.execute(q_short)
    results.append([x for x in cursor.fetchall()])
    conn.close()
  return render_template("results.jinja2", results=results)
def discuss():
  return render_template('discuss.jinja2', active='discuss')

def skratenici():
  return render_template("skratenici.html")

def predgovor():
  return render_template("predgovor")

def policy():
  return render_template("policy.jinja2")
