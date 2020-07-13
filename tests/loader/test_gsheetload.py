import unittest

import pandas as pd

from api.utils.loader import load_gsheet, DataSourceProtocol
from api.utils.loader import load

import logging

tlog = logging.getLogger(__name__)


class LoaderTest(unittest.TestCase):
    
    def setUp(self):
        self.save_result = True
        self.loader = "gsheet"
        self.gsheet_url = 'https://docs.google.com/spreadsheets/d/11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do/edit#gid=1988095192'
        self.gsheet_key = '11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do'
        self.sheet_id = 1988095192


    def test_protocol_url(self):
        ds = DataSourceProtocol()
        assert 'https://' in ds.gen_url(dtype='csv', key=self.gsheet_key, sheet=self.sheet_id)

    def test_gsheet_download_with_key(self):
        tlog.info('Running Gsheet Download Test')
        print(load_gsheet(key=self.gsheet_key, sheet=self.sheet_id))

    
    # def test_explicit_loader(self):

    #     output = load(
    #         file_or_buffer=file_url,
    #         loader=loader,
    #         max_len=371,
    #     )
    #     self.assertIsNotNone(output)
        
    #     if self.save_result:
    #         filename = '_'.join([category, loader])
    #         output.to_csv(filename)