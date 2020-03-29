
"""
Basic unittests for API

Special thanks to Bob from PyBites
https://pybit.es/simple-flask-api.html
"""

from flask_testing import LiveServerTestCase
import unittest
import json
import requests

from api import create_app

# LIVE_URL = 'http://127.0.0.1:5000/'
# DATA_URLS = []



class LocalServerTest(LiveServerTestCase):

    def create_app(self):
        app = create_app()
        return app

    def test_server_is_up_and_running(self):
        response = requests.get(self.get_server_url())
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_mock_urls(self):
        MOCK_URLS = [f'{self.get_server_url()}/mock{i}' for i in [1, 2]]
        for url in MOCK_URLS:
            print('Searching {}'.format(url))
            response = requests.get(url)
            self.assertEqual(response.status_code, 200)


class DeployedServerTest(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()