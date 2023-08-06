# coding=utf-8
"""Tyko library."""
__version__ = '0.1b1'

import netrc
import os
from urllib.parse import urljoin, urlparse

import requests

_TYKO_KEY = 'TYKO_KEY'


class Tyko:
    """Main class for reporting to Tyko."""

    _hostname = 'api.tyko.ai'
    _prefix_url: str
    _session: requests.Session
    _cur_key: str

    def _get_new_key(self) -> str:
        res = self._session.post(self._fix_url('/v1/keys/'))
        return res.json()['key']

    def _resolve_key(self, netrc_file: str = None):
        if not hasattr(self, '_cur_key'):
            if _TYKO_KEY in os.environ:
                self._cur_key = os.environ[_TYKO_KEY]
            else:
                try:
                    netrc_ = netrc.netrc(netrc_file)
                except FileNotFoundError:
                    netrc_ = None
                if netrc_ is not None and self._hostname in netrc_.hosts:
                    self._cur_key = netrc_.hosts[self._hostname][2]
                else:
                    self._cur_key = self._get_new_key()
                    print(f'A new key was created: {self._cur_key}') # noqa

        return self._cur_key

    def _headers(self):
        self._resolve_key()

    def _fix_url(self, url: str) -> str:
        return urljoin(self._prefix_url, url)

    def _get(self, url: str) -> requests.Response:
        """GET request to the backend."""
        return self._session.get(self._fix_url(url))

    def _post(self, url: str, data: dict = None):
        """POST request to the backend."""
        return self._session.post(self._fix_url(url), json=data)

    @property
    def key(self) -> str:
        """Return the API key used by the current instance."""
        return self._resolve_key()

    def __init__(self, project: str, desc: str = None, prefix_url: str = None):
        """Nothing here."""
        if prefix_url is None:
            prefix_url = 'https://api.tyko.ai'

        """Keep track of prefix url."""
        self._session = requests.Session()
        self._prefix_url = prefix_url
        self._hostname = urlparse(prefix_url).hostname
        self._resolve_key()
