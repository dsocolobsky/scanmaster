from api import app
from random import randint
import time
import api.database as db
import api.scripts

@app.route('/')
def index():
    return 'API INDEX'

@app.route('/hosts')
def ips():
    hosts = db.hosts()
    return {'hosts': hosts}

@app.route('/test')
def test():
    return {'port': randint(1, 512)}

@app.route('/isup/<ip>')
def isup(ip):
    res = True if randint(0,1) == 0 else False
    return {'up': res}

@app.route('/rebuild')
def rebuild():
    api.scripts.rebuild()