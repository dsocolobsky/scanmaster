from datetime import datetime

from pony import orm

db = orm.Database()
orm.set_sql_debug(True)
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)


class Host(db.Entity):
    ip = orm.PrimaryKey(str)
    name = orm.Optional(str)
    isup = orm.Optional(bool)
    os = orm.Optional(str)
    os_acc = orm.Optional(int)
    ports = orm.Optional(orm.IntArray)
    services = orm.Set("Service")
    initial_scan = orm.Optional(datetime)
    last_scan = orm.Optional(datetime)
    notes = orm.Optional(orm.LongStr)


class Service(db.Entity):
    port = orm.Required(int)
    protocol = orm.Optional(str)
    fingerprint = orm.Optional(str)
    name = orm.Optional(str)
    hasPicture = orm.Required(bool)
    picture = orm.Optional(orm.LongStr)
    host = orm.Required(Host)


db.generate_mapping(create_tables=True)


@orm.db_session
def hosts():
    hosts = []
    for h in Host.select():
        hosts.append(h.to_dict(with_lazy=True))
    return hosts


@orm.db_session
def hosts_ip():
    hosts = []
    for h in Host.select():
        hosts.append(h.ip)
    return hosts


@orm.db_session
def host_by_ip(ip):
    try:
        found = Host[ip]
    except orm.ObjectNotFound:
        found = None

    return found


def host_setprop(host, prop, val):
    host[prop] = val
    orm.commit()


def change_host_name(ip, name):
    host = Host[ip]
    host.name = name
    orm.commit()
