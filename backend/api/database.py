from pony import orm

db = orm.Database()
orm.set_sql_debug(True)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Host(db.Entity):
    ip = orm.PrimaryKey(str)
    isup = orm.Optional(bool)
    os = orm.Optional(str)
    os_acc = orm.Optional(int)
    ports = orm.Optional(orm.IntArray)
    services = orm.Set('Service')

class Service(db.Entity):
    port = orm.Required(int)
    protocol = orm.Optional(str)
    fingerprint = orm.Optional(str)
    name = orm.Optional(str)
    hasPicture = orm.Required(bool)
    host = orm.Required(Host)

db.generate_mapping(create_tables=True)

@orm.db_session
def hosts():
    hosts = []
    for h in Host.select():
        hosts.append(h.to_dict())
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