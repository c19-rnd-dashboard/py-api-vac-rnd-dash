"""
Basic unittests for Various Tranform Helper Functions

Special thanks to Flask!
https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/
"""

from flask_testing import LiveServerTestCase
import unittest
import json
import requests
import sys
import os
from io import StringIO

from api import create_app
from api.db import get_db, get_session, init_db
from api.utils.transform.transforms import get_product_names

# LIVE_URL = 'http://127.0.0.1:5000/'
# DATA_URLS = []

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as file:
    _data_sql = file.read().decode('utf8')

class LocalDatabaseTest(LiveServerTestCase):

    def create_app(self):
        app = create_app()
        return app
        
    def test_get_product_names(self):
        print(get_product_names())
        
