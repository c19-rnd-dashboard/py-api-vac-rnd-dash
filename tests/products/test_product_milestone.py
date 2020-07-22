import unittest

from api.utils.transform import milestone_transformer
from api.utils.loader import load

import pandas as pd

import os


class ProductMilestoneTransform(unittest.TestCase):

    def setUp(self):
        loader = "gsheet"
        gsheet_url = 'https://docs.google.com/spreadsheets/d/11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do/edit#gid=1988095192'

        self.data = load(
            file_or_buffer=gsheet_url,
            loader=loader,
        )

        self.save = False


    def test_product_milestone_transform(self):
        output = milestone_transformer(self.data)
        self.assertIsNotNone(output)

        if self.save:
            savepath = os.path.join(os.getcwd(), 'test_product_contact_transform.csv')
            output.to_csv(savepath, index=False)
