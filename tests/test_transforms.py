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
import pandas as pd

from api import create_app
from api.db import get_db, get_session, init_db
from api.utils.transform import get_product_names, milestone_transformer
from api.utils.loader import load


from api.utils.transform import clean_country


class LocalDatabaseTest(LiveServerTestCase):
    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        self.test_frame = pd.read_csv('/home/vbrandon/Bin/py-api-vac-rnd-dash/data/vaccines/vaccineworkfile4.csv')

    def test_get_product_names(self):
        self.assertIsNotNone(get_product_names())

    def test_explicit_loader(self):
        loader = "unfiltered_csv"
        file_url = 'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile4.csv'
        output = load(
            file_or_buffer=file_url,
            loader=loader,
            max_len=371,
        )
        self.assertIsNotNone(output)


class CommonObjectStandardizationTest(unittest.TestCase):

    def setUp(self):
        self.set_countries_null = ''
        self.set_countries_null_multiple = ','
        self.set_countries_full = 'Japan, japn, Korea, north korea, amsterdam, Amstrdam'

    def test_null_countries(self):
        self.assertIsNone(clean_country(self.set_countries_null))
        self.assertIsNone(clean_country(self.set_countries_null_multiple))