import unittest

import pandas as pd

from api.utils.loader import load


class LoaderTest(unittest.TestCase):
    
    def setUp(self):
        self.save_result = True
    
    
    def test_explicit_loader(self):
        category = "products"
        loader = "unfiltered_csv"
        file_url = 'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile4.csv'
        output = load(
            file_or_buffer=file_url,
            loader=loader,
            max_len=371,
        )
        self.assertIsNotNone(output)
        
        if self.save_result:
            filename = '_'.join([category, loader])
            output.to_csv(filename)