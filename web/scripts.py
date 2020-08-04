import os
import subprocess
from pony import orm
from .database import Host, Service, db, host_by_ip
import xml.etree.ElementTree as ET
from datetime import datetime as dt


def parse_list(path):
    scans = []
    with open(path) as file:
        # ignore the first line
        file.readline()
        while (line := file.readline())[0] != "#":
            data = line.split()
            ip = data[3]
            port = int(data[2])
            scans.append((ip, port))

    print(scans)
    return scans


def masscan_range(range, ports):
    print(f"masscaning {range} ports: {ports}")
    ports_s = f"-p{ports}"
    subprocess.run(
        ["sudo", "masscan", ports_s, range, "-oL", "out.txt"], stdout=subprocess.DEVNULL
    )

    scans = parse_list("out.txt")
    os.remove("out.txt")
    return scans


# TODO don't use ORM here and move to database code
@orm.db_session
def scans_to_db(scans):
    for scan in scans:
        ip, port = scan
        print(f"Finding {ip}")
        try:
            found = Host[ip]
        except orm.ObjectNotFound:
            print("None")
            h = Host(
                ip=ip, name=ip, ports=[port], initial_scan=dt.now(), last_scan=dt.now()
            )
            s = Service(port=port, hasPicture=False, host=h)
        else:
            print("Existed")
            if port not in found.ports:
                found.ports.append(port)
                s = Service(port=port, hasPicture=False, host=found)

    orm.commit()


def rebuild():
    scans = parse_list("testlist")
    scans_to_db(scans)


def ping_ip(ip):
    cmd = ["ping", "-c", "1", ip]
    return subprocess.call(cmd) == 0


class NmapPortInfo:
    port = None
    protocol = ""
    service = ""
    fingerprint = ""


class NmapHostInfo:
    ip = None
    os = None
    os_acc = None
    ports = []


def parse_nmap_xml(fname, ip):
    print(f"Loading {fname} to parse XML")
    tree = ET.parse(fname)
    if tree is None:
        print("TREE IS NONE")
        return None

    root = tree.getroot().find("host")
    if root is None:
        print("ROOT IS NONE")
        return None

    info = NmapHostInfo()
    info.ip = ip

    print("REACHED HERE")
    os_info = root.find("os").findall("osmatch")[0].attrib
    print("REACHED HERE 2")
    info.os = os_info["name"]
    info.os_acc = os_info["accuracy"]

    print("REACHED HERE 3")
    ports_node = root.find("ports")
    for port in ports_node.findall("port"):
        print("Found port")
        port_info = NmapPortInfo()
        port_info.port = int(port.attrib["portid"])
        port_info.protocol = port.attrib["protocol"]
        service = port.find("service").attrib
        port_info.service = service["name"]
        if "servicefp" in service:
            port_info.fingerprint = service["servicefp"]

        info.ports.append(port_info)

    return info


# TODO move to class Service
@orm.db_session
def service_from_port_info(info, host, service=None):
    if service is None:
        print("Service was none")
        service = Service(port=info.port, hasPicture=False, host=host)

    print(f"SERVINFO: {service.name}, {service.protocol}")
    service.port = info.port
    service.protocol = info.protocol

    service.name = info.service
    if service.name == "http-alt":
        service.name = "http"

    service.fingerprint = info.fingerprint
    service.hasPicture = False
    service.host = host

    return service


@orm.db_session
def host_info_to_db(info):
    print("host info to DB")
    host = Host[info.ip]
    host.isup = True  # Since we just scanned host must be up
    host.os = info.os
    host.os_acc = info.os_acc

    for port in info.ports:
        print(f"Looking for port {port.port}")
        query = host.services.select(lambda s: s.port == port.port)[:]
        if len(query) == 0:
            print("Not found")
            service = service_from_port_info(port, host)
            host.ports.append(port.port)
        else:
            print("Did found")
            service = query[0]
            service_from_port_info(port, host, service)

    orm.commit()


def nmap(ip, fast):
    host = host_by_ip(ip)
    if host is None:
        print("ip was none")
        host = Host(
            ip=ip, name=ip, ports=[]
        )  # TODO create create_host in db as wrapper
        orm.commit()

    print(f"nmapping {ip}, fast={fast}")
    arg = "-F" if fast else None
    fname = f"nmap_out/{ip}.xml"

    print("Running nmap")
    subprocess.run(
        [
            "sudo",
            "nmap",
            arg,
            "-A",
            "-sV",
            "--version-intensity",
            "5",
            ip,
            "-oX",
            fname,
        ],
        stdout=subprocess.DEVNULL,
    )
    print("Ran NMAP")

    # fname = '190.122.144.191.xml'
    info = parse_nmap_xml(fname, ip)
    print("Parsed XML")
    if info is None:
        print("Info was none")
        host.isup = False
        orm.commit()
        return False

    host_info_to_db(info)
    return True
