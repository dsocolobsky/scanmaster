from web import app
from random import randint
import time
import web.database as db
import web.scripts
from flask import render_template

@app.route('/')
def index():
    hosts = db.hosts()
    return render_template('index.html', hosts=hosts)

@app.route('/host/<ip>')
def host(ip):
    host = db.host_by_ip(ip)
    return render_template('host.html', host=host)

@app.route('/test')
def test():
    return {'port': randint(1, 512)}

@app.route('/isup/<ip>')
def isup(ip):
    res = True if randint(0,1) == 0 else False
    return {'up': res}

@app.route('/rebuild')
def rebuild():
    web.scripts.rebuild()