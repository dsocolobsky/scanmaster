from web import app
from random import randint
import time
import web.database as db
import web.scripts
from flask import render_template, redirect, url_for, request
from pony import orm

@app.route('/')
def index():
    hosts = db.hosts()
    return render_template('index.html', hosts=hosts)

@app.route('/host/<ip>')
def host(ip):
    host = db.host_by_ip(ip).to_dict()
    return render_template('host.html', host=host)

@app.route('/test')
def test():
    return {'port': randint(1, 512)}

@orm.db_session
@app.route('/ping/<ip>', methods=['POST'])
def ping(ip):
    host = db.Host[ip]
    res = web.scripts.ping_ip(ip)

    host.isup = res
    orm.commit()

    return {'up': res}


@app.route('/nmap/<ip>', methods=['POST'])
def nmap(ip):
    res = web.scripts.nmap(ip, fast=True)
    s = 'okay' if res else 'error'
    print(s)
    return s

@app.route('/host/<ip>/change/name', methods=['POST'])
def changename(ip):
    name = request.form['name']
    if name is None:
        print("name was none")
        return "name was none"

    db.change_host_name(ip, name)
    return "okay"

@app.route('/rebuild')
def rebuild():
    web.scripts.rebuild()
