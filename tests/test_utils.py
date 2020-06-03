"""
Basic Unittests for application utilities

    Load, Parse -> Ingest Pipeline
"""

from flask_testing import LiveServerTestCase
import unittest
from api.utils import run_ingest
from data import factory_countries, factory_milestones

from api import create_app

class IngestTest(LiveServerTestCase):
    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        self.test_trial_url = 'https://raw.githubusercontent.com/ebmdatalab/covid_trials_tracker-covid/master/notebooks/processed_data_sets/trial_list_2020-05-26.csv'
        self.test_product_url = 'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile3.csv'
        self.test_factory_milestones = factory_milestones
        self.test_factory_countries = factory_countries

    def test_trial_ingest(self):
        category = 'trial'
        error = run_ingest(source=self.test_trial_url, category=category)
        self.assertIsNone(error)

    def test_explicit_ingest(self):
        category = 'product'
        loader = "unfiltered_csv"
        error = run_ingest(source=self.test_product_url, category=category, loader=loader, max_len=923)
        self.assertIsNone(error)

    def test_object_ingest_countries(self):
        error_a = run_ingest(source=self.test_factory_countries, category='country')
        self.assertIsNone(error_a)

    def test_object_ingest_milestones(self):
        error_b = run_ingest(source=self.test_factory_milestones, category='milestone')
        self.assertIsNone(error_b)


if __name__ == "__main__":
    unittest.main()