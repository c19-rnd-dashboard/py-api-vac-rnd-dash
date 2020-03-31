"""
Basic Unittests for application utilities

    Load, Parse -> Ingest Pipeline
"""

import unittest
from api.utils import run_ingest

class IngestTest(unittest.TestCase):
    """ Tests for Deployed Server """
    def setUp(self):
        self.test_url = 'https://raw.githubusercontent.com/ebmdatalab/covid_trials_tracker-covid/master/notebooks/processed_data_sets/trial_list_2020-03-25.csv'

    def test_trial_ingest(self):
        category = 'trial'
        run_ingest(source=self.test_url, category=category)

if __name__ == "__main__":
    unittest.main()