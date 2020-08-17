# test_loadcache.py

import unittest

from api.utils.loader import (
    load, cache_source, check_cache, read_cache, clear_cache,
)

from api.utils.loader.loaders import FileLoader

import pandas as pd

import os


class LoadCacheTest(unittest.TestCase):

    def setUp(self):
        self.loader = "gsheet"
        self.gsheet_url = 'https://docs.google.com/spreadsheets/d/11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do/edit#gid=1988095192'

        self.save = False


    def test_cache_source(self):
        loader = FileLoader(
            filename=self.gsheet_url,
            loader=self.loader,
            cache=False,
        )
        data = loader.fetch_transform()
        cache_source(name=self.gsheet_url, data=data)
        self.assertEqual(True, clear_cache())  #  Currently eliminates entire cache (not specific to file)


    def test_clear_cache(self):
        pass



    def test_cache_read(self):
        pass
    
