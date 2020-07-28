import os
import subprocess
from pony import orm
from .database import Host, Service

def parse_list(path):
    scans = []
    with open(path) as file:
        # ignore the first line
        file.readline()
        while (line := file.readline())[0] != '#':
            data = line.split()
            ip = data[3]
            port = int(data[2])
            scans.append((ip, port))

    print(scans)
    return scans

def masscan_range(range, ports):
    print(f'masscaning {range} ports: {ports}')
    ports_s = f'-p{ports}'
    subprocess.run(['sudo', 'masscan', ports_s, range, '-oL', 'out.txt'], 
        stdout=subprocess.DEVNULL)

    scans = parse_list('out.txt')
    os.remove('out.txt')
    return scans

# TODO don't use ORM here and move to database code
@orm.db_session
def scans_to_db(scans):
    for scan in scans:
        ip, port = scan
        print(f'Finding {ip}')
        try:
            found = Host[ip]
        except orm.ObjectNotFound:
            print('None')
            h = Host(ip=ip, ports=[port])
            s = Service(port=port, hasPicture=False, host=h)
        else:
            print('Existed')
            if port not in found.ports:
                found.ports.append(port)
                s = Service(port=port, hasPicture=False, host=found)
            
    orm.commit()

def rebuild():
    scans = parse_list('testlist')
    scans_to_db(scans)