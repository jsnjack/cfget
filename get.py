#!/usr/bin/env python3
import requests
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from collections import OrderedDict
from urllib3.util.ssl_ import create_urllib3_context, DEFAULT_CIPHERS

URL = "https://www.transunion.com/"

DEFAULT_CIPHERS = "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:ECDH+AESGCM:DH+AESGCM:ECDH+AES:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!eNULL:!MD5:!DSS:!ECDHE+SHA:!AES128-SHA:!AESCCM:!DHE:!ARIA"

DEFAULT_HEADERS = OrderedDict(
    (
        # ("Host", None),
        # ("Connection", "keep-alive"),
        # ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", "any"),
        # (
        #     "Accept",
        #     "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # ),
        # ("Accept-Language", "en-US,en;q=0.9"),
        # ("Accept-Encoding", "gzip, deflate"),
    )
)


class CFAdapter(HTTPAdapter):
    """ HTTPS adapter that creates a SSL context with custom ciphers """

    def get_connection(self, *args, **kwargs):
        conn = super(CFAdapter, self).get_connection(*args, **kwargs)

        context = create_urllib3_context(ciphers=DEFAULT_CIPHERS)
        conn.conn_kw["ssl_context"] = context

        return conn


def main():
    session = Session()
    session.mount("https://", CFAdapter())
    resp = session.get(URL, headers=DEFAULT_HEADERS)
    print(resp.status_code, len(resp.content))

    resp = requests.get(URL, headers={"User-Agent": "any"})
    print(resp.status_code, len(resp.content))


if __name__ == "__main__":
    main()
