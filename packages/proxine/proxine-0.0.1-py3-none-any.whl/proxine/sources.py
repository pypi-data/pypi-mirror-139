"""
Each get function in this module returns a list of strings "{ip}:{port}".
"""
import requests
from lxml import etree
from selenium import webdriver

from proxine.settings import PROXINE_TIMEOUT


headers = {
    "User-Agent": "Mozilla/5.0",
}


def get_all():
    ps = []
    # ps += get_free_proxy_list()
    # ps += get_openproxy()
    ps += get_proxy_scrape()
    # ps += get_spys_one()
    return sorted(set(ps))


def get_file(filename):
    with open(filename) as f:
        proxies = [p.strip() for p in f.read().split() if p.strip()]
        # proxies = [dict(zip(["ip", "port"], p.strip().split(":")))
        #            for p in f.read().split() if p.strip()]
    return proxies


def _convert_pl(proxy_list):
    """Convert list of dicts {ip, port} into list of strings [ip:port]."""
    return [f"{p['ip']}:{p['port']}" for p in proxy_list]


def get_free_proxy_list():
    url = "https://free-proxy-list.net/"
    # this list is a subset:
    # url = "https://www.sslproxies.org/"
    r = requests.get(url, headers=headers, timeout=PROXINE_TIMEOUT)

    tree = etree.fromstring(r.text, parser=etree.HTMLParser())
    table = tree.xpath("//div[contains(@class, 'fpl-list')]/table")[0]
    keys = table.xpath("thead/tr/th/text()")
    # keys = [
    #     "ip",
    #     "port",
    #     "code",
    #     "country",
    #     "anon",
    #     "google",
    #     "https",
    #     "last_check",
    # ]

    proxies = []
    for row in table.xpath("tbody/tr"):
        values = [d.text for d in row.xpath("td")]
        p = dict(zip(keys, values))
        proxy = {
            "ip": p["IP Address"],
            "port": p["Port"],
            "ssl": (p["Https"] == "yes"),
            # "country": p["Port"],
        }
        proxies.append(proxy)

    return _convert_pl(proxies)


def get_openproxy():
    url = "https://api.openproxy.space/lists/http"
    r = requests.get(url, headers=headers, timeout=PROXINE_TIMEOUT)
    proxies = [proxy for d in r.json()["data"] for proxy in d["items"]]
    return proxies


def get_proxy_scrape():
    url = (
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http"
        "&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true"
    )
    r = requests.get(url, headers=headers, timeout=PROXINE_TIMEOUT)
    proxies = r.text.split()
    return proxies


def get_spys_one():
    url = "https://spys.one/en/https-ssl-proxy/"
    o = webdriver.firefox.options.Options()
    o.headless = True
    browser = webdriver.Firefox(options=o)
    browser.get(url)
    html = browser.page_source
    # with open("spys_one.html", "w") as f:
    #     f.write(html)
    tree = etree.fromstring(html, parser=etree.HTMLParser())
    ps = tree.xpath("//tr[contains(@class,'spy1x')]/td[1]/font/text()")[1:]
    ips, ports = ps[::2], ps[1::2]
    proxies = [":".join(t) for t in zip(ips, ports)]
    # rows = tree.xpath("//tr[contains(@class,'spy1x')]")
    return proxies
