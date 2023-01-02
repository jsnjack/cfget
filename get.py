#!/usr/bin/env python3
import requests
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from collections import OrderedDict
from urllib3.util.ssl_ import create_urllib3_context, DEFAULT_CIPHERS

URL = "http://transunion.com/"

DEFAULT_CIPHERS += ":!ECDHE+SHA:!AES128-SHA:!AESCCM:!DHE:!ARIA"

DEFAULT_HEADERS = OrderedDict(
    (
        ("Host", None),
        ("Connection", "keep-alive"),
        ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"),
        (
            "Accept",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        ),
        ("Accept-Language", "en-US,en;q=0.9"),
        ("Accept-Encoding", "gzip, deflate"),
    )
)


class CFAdapter(HTTPAdapter):
    """ HTTPS adapter that creates a SSL context with custom ciphers """

    def get_connection(self, *args, **kwargs):
        conn = super(CFAdapter, self).get_connection(*args, **kwargs)

        if conn.conn_kw.get("ssl_context"):
            conn.conn_kw["ssl_context"].set_ciphers(DEFAULT_CIPHERS)
        else:
            context = create_urllib3_context(ciphers=DEFAULT_CIPHERS)
            conn.conn_kw["ssl_context"] = context

        return conn


def main():
    headers = OrderedDict(DEFAULT_HEADERS)
    session = Session()
    session.headers = headers
    session.org_method = None
    session.mount("https://", CFAdapter())
    resp = session.get(URL)
    print(resp.status_code)

    resp = requests.get(URL)
    print(resp.status_code)


if __name__ == "__main__":
    main()
