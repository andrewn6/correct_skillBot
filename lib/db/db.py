from os.path import isfile
import psycopg2
import urllib.parse as urlparse
import os
from apscheduler.triggers.cron import CronTrigger
from config import *

BUILD_PATH = "./data/db/build.sql"
#TODO : get url from os env
url = urlparse.urlparse(DATABASE_URL) #os.environ['DATABASE_URL']
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

cxn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
cur = cxn.cursor()

def with_commit(func):
    def inner(*args,**kwargs):
        func(*args,**kwargs)
        commit()
    return inner

@with_commit
def build():
	if isfile(BUILD_PATH):
		scriptexec(BUILD_PATH)

def commit():    
    # debug msg print("committing .... to db")
    cxn.commit()

def autosave(sched):
    sched.add_job(commit,CronTrigger(second=0))

def close():
    cxn.close()

def field(command,*values):
    cur.execute(command,tuple(values))

    if (fetch := cur.fetchone()) is not None:

        return fetch[0]

def record(command,*values):
    cur.execute(command,tuple(values))

    return cur.fetchone()

def records(command,*values):
    cur.execute(command,tuple(values))

    return cur.fetchall()

def column(command,*values):
    cur.execute(command,tuple(values))

    return [item[0] for item in cur.fetchall()]
 
def execute(command, *values):
	cur.execute(command, tuple(values))


def multiexec(command, valueset):
	cur.executemany(command, valueset)


def scriptexec(path):
	with open(path, "r", encoding="utf-8") as script:
		cur.execute(script.read())


