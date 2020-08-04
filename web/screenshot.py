from .database import Host, Service, db, host_by_ip
from pony import orm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time

SELENIUM_DRIVER = "chromedriver"


def screenshot_web(driver, host):
    ip, port = host
    url = f"http://{ip}:{port}"
    print(f"Screenshoting {url}")
    try:
        driver.get(url)
    except TimeoutException:
        print("Timeouted!")
        return None
    else:
        print("Screenshot delay START")
        time.sleep(4)
        b64 = driver.get_screenshot_as_base64()
        print("Screenshot DONE")
        print(b64)
        return b64
        # driver.save_screenshot(f"static/img/screenshots/{ip}:{port}.png")
        # return True


@orm.db_session
def screenshot_single_host(ip):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(SELENIUM_DRIVER, chrome_options=opts)
    driver.set_page_load_timeout(15)

    host = Host[ip]
    for port in host.ports:
        b64 = screenshot_web(driver, (host.ip, port))
        if b64 is None:
            continue

        s = Service.get(lambda s: s.port == port and s.host.ip == ip)
        if s is None:
            print(f"{ip} : {port} not found when screenshot")
        else:
            s.hasPicture = True
            s.picture = b64

    orm.commit()
    driver.quit()


@orm.db_session
def screenshot_hosts(hosts):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(SELENIUM_DRIVER, chrome_options=opts)
    driver.set_page_load_timeout(15)

    for host in hosts:
        ip, port = host
        res = screenshot_web(driver, host)
        if not res:
            continue

        s = Service.get(lambda s: s.port == port and s.host.ip == ip)
        if s is None:
            print(f"{ip} : {port} not found when screenshot")
        else:
            s.hasPicture = True

    orm.commit()
    driver.quit()
