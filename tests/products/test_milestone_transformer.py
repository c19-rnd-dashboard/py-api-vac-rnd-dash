import unittest

from api.utils.transform import milestone_transformer

import pandas as pd

import os


class ProductPipleTest(unittest.TestCase):

    def setUp(self):
        self.data = pd.read_csv(
            os.path.join(os.getcwd(), 'tests', 'products', 'products_unfiltered_csv.csv'))

        # TODO: implement external test config
        self.dumpfile = True



    def test_product_raw_transform(self):
        tdata = milestone_transformer(self.data)
        self.assertIsNotNone(tdata)

        tdata.to_csv('transformer_test.csv', index=False)
        
