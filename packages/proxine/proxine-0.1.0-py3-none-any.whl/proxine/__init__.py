import re

PROXY_FORMAT = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+")


def _parse_proxy(proxy_string):
    try:
        ip, port = proxy_string.strip().split(":")
        return {
            "ip": ip,
            "port": port,
        }
    except (AttributeError, ValueError):
        return {}


class Proxy(dict):
    """
    Class to represent a proxy in a handy way. The attributes are dict keys and
    the string representation is the usual "{ip}:{port}" format.

    The required attributes are `ip` and `port`. Any extra keyword arguments in
    the init call will be stored in their own keys. Thus you can add `country`
    for example.
    """

    def __init__(self, proxy_string=None, **kwargs):
        """
        You can either pass a `proxy_string` like "1.2.3.4:5", or pass "ip" and
        "port" keyword arguments. Note: `proxy_string` overrides keyword args.

        If the first positional argument is a dict instead of string, its items
        will be expanded as keyword arguments, overriding them.
        """
        super().__init__()
        if type(proxy_string) is dict:
            kwargs.update(**proxy_string)
            proxy_string = None
        self.update(**kwargs)
        self.update(**_parse_proxy(proxy_string))
        if not self._check_format():
            raise ValueError(f"Invalid proxy format: {self}")

    def _check_format(self):
        proxy = str(self)
        a = [proxy] == PROXY_FORMAT.findall(proxy)
        if a:
            b = True
            for n in self["ip"].split("."):
                b &= int(n) < 256
            return a and b
        else:
            return False

    def to_string(self):
        """Alias for `str(self)`."""
        return str(self)

    def __repr__(self):
        return f"{self.get('ip')}:{self.get('port')}"

    def __hash__(self):
        return str(self).__hash__()
