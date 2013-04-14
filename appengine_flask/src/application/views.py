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
  return render_template("index.jinja2")

def search():
  conn = get_connection()
  cursor = conn.cursor()
  key = "mkd"
  if request.args.get("from_lang"):
    key_n = request.args.get("from_lang")
    if key_n in match_col:
      key =key_n
  s_pat= request.args.get("Search")
  q_long=u"SELECT * FROM word WHERE MATCH(%s) AGAINST ('%s')"%(match_col[key], s_pat)
  q_short = u"SELECT * FROM word where windex like '%(search)s %%' or windex like '%% %(search)s ' or windex like '%% %(search)s'"%{"search":s_pat}
  if len(s_pat)>3:
    cursor.execute(q_long)
  else:
    cursor.execute(q_short)
  rows = cursor.fetchall()
  conn.close()
  return render_template("results.jinja2", rows=rows)

def skratenici():
  return render_template("skratenici.html")

def predgovor():
  return render_template("predgovor")
