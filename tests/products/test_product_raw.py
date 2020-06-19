import unittest

from api.utils.transform import clean_product_raw

import pandas as pd

import os


class ProductPipleTest(unittest.TestCase):

    def setUp(self):
        self.data = pd.read_csv(
            os.path.join(os.getcwd(), 'tests', 'products', 'products_unfiltered_csv.csv'))


    def test_product_raw_transform(self):
        self.assertIsNotNone(clean_product_raw(self.data))