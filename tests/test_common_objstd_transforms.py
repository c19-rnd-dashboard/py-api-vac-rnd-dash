"""
Basic unittests for Various Tranform Helper in Common object standardization
"""

import unittest
from api.utils.transform import clean_country



class CommonObjectStandardizationTest(unittest.TestCase):

    def setUp(self):
        self.set_countries_null = ''
        self.set_countries_null_multiple = ','
        self.set_countries_simple = 'United States, united kingdom'
        self.set_countries_with_null = 'Australia,, United States'
        self.set_countries_full = 'Japan, japn, Korea, north korea, netherlands'
        self.set_countries_with_hypen = 'United State, Rome-Italy'
        self.set_default_null_name = 'Japan, NA, N/A'

    def test_null_countries(self):
        self.assertIsNone(clean_country(self.set_countries_null)['alpha3'])
        self.assertIsNone(clean_country(self.set_countries_null_multiple)['alpha3'])

    def test_country_lookup(self):
        print(clean_country(self.set_countries_simple))
        print(clean_country(self.set_countries_full))
        
        # Test with partial null fields
        lc = clean_country(self.set_countries_with_null)
        print(lc)

    def test_country_lookup_multi_delimiter(self):
        testset = self.set_countries_with_hypen
        self.assertEqual(len(testset.split(',')), len(clean_country(testset)['alpha3'].split(',')))

    def test_country_lookup_null_placeholder(self):
        testset = self.set_default_null_name
        print(clean_country(testset))
        self.assertEqual(1, len(clean_country(testset)['alpha3'].split(',')))
        