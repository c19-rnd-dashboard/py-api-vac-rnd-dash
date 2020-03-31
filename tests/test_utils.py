"""
Basic Unittests for application utilities

    Load, Parse -> Ingest Pipeline
"""

from flask_testing import LiveServerTestCase
import unittest
from api.utils import run_ingest

from api import create_app

class IngestTest(LiveServerTestCase):
    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        self.test_url = 'https://raw.githubusercontent.com/ebmdatalab/covid_trials_tracker-covid/master/notebooks/processed_data_sets/trial_list_2020-03-25.csv'

    def test_trial_ingest(self):
        category = 'trial'
        error = run_ingest(source=self.test_url, category=category)
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()