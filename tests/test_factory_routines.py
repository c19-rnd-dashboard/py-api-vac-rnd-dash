"""
Test methods packaged with factory reference data
"""

import unittest
from data import build_alpha2_index, build_name_index, lookup_alpha3_countrycode





class CountryReferenceTest(unittest.TestCase):
    
    def setUp(self):
        self.test_data = [
            {'name': 'South Africa', 'alpha2': 'ZA', 'alpha3': 'ZAF'}, 
            {'name': 'South Georgia and the South Sandwich Islands', 'alpha2': 'GS', 'alpha3': 'SGS'}, 
            {'name': 'Spain', 'alpha2': 'ES', 'alpha3': 'ESP'}, 
            {'name': 'Sri Lanka', 'alpha2': 'LK', 'alpha3': 'LKA'}, 
            {'name': 'Sudan', 'alpha2': 'SD', 'alpha3': 'SDN'}, 
            {'name': 'Suri', 'alpha2': 'SR', 'alpha3': 'SUR'}, 
            {'name': 'Svalbard and Jan Mayen', 'alpha2': 'SJ', 'alpha3': 'SJM'}, 
            {'name': 'Swaziland', 'alpha2': 'SZ', 'alpha3': 'SWZ'}, 
            {'name': 'Sweden', 'alpha2': 'SE', 'alpha3': 'SWE'}, 
            {'name': 'Switzerland', 'alpha2': 'CH', 'alpha3': 'CHE'}, 
            {'name': 'Syrian Arab Republic', 'alpha2': 'SY', 'alpha3': 'SYR'},
        ]

    
    def test_name_index_construction(self):
        cname_index = build_name_index(self.test_data)
        self.assertEqual('ZA', cname_index['South Africa']['alpha2'])

    
    def test_alpha2_index_construction(self):
        alpha2_index = build_alpha2_index(self.test_data)
        self.assertEqual('LKA', alpha2_index['LK']['alpha3'])


    def test_lookup_alpha3(self):
        result = lookup_alpha3_countrycode('ES')
        self.assertEqual('ESP', result)