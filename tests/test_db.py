"""
Basic unittests for DataBase

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

# LIVE_URL = 'http://127.0.0.1:5000/'
# DATA_URLS = []

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as file:
    _data_sql = file.read().decode('utf8')

class LocalDatabaseTest(LiveServerTestCase):

    def create_app(self):
        app = create_app()
        return app
        
    def test_get_db(self):
        db = get_db()
        assert db is get_db()

    def test_session_context(self):
        with get_session() as session:
            session.execute('SELECT 1')

    def test_init_db_command(self):
        out = StringIO()
        init_db(out)
        output = out.getvalue().strip()
        print('init-db output: ', output)
        self.assertIn('init', output)

    def test_sql_write_read_session(self):
        print(_data_sql)
        with get_session() as session:
            # Note:  There is no commit operation occuring here, so this data won't be written to the database
            session.execute(_data_sql)
            test_result = session.execute('SELECT * FROM productraw p;').fetchone()
            self.assertNotEqual(test_result, None)
            # session.commit()  # DEBUG: see if write can be committed by session

