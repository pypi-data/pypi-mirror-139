# noqa
import unittest
import os
from unittest import mock
from unittest.mock import patch
import requests_mock

from tyko import Tyko


class BaseTestCase(unittest.TestCase):

    def setUp(self):

        # Default mock of the API.
        self._api_mock = requests_mock.Mocker()
        self._api_mock.post(
            "https://api.tyko.ai/v1/keys/", json={"key": "key"}
        )
        self._api_mock.start()

    def tearDown(self):
        self._api_mock.stop()

    def test_base(self):
        assert True, "This is a simple test."

    @patch('netrc.open', mock.Mock(side_effect=FileNotFoundError))
    def test_netrc_not_found(self):
        tyko = Tyko(project="my-project")
        assert tyko.key == "key", "Obtain a new key."

    def test_new_key(self):
        tyko = Tyko(project="my-project")
        assert tyko.key == "key", "Obtain a new key."

    @mock.patch.dict(os.environ, {"TYKO_KEY": "yyy"}, clear=True)
    def test_key_from_env(self):
        tyko = Tyko(project="my-project")
        assert tyko.key == "yyy", "Get the key from env variables."


class LiveTestCase(unittest.TestCase):
    @patch('netrc.open', mock.Mock(side_effect=FileNotFoundError))
    def test_new_key(self):
        tyko = Tyko(project="my-project")
        self.assertEqual(len(tyko.key), 64)
