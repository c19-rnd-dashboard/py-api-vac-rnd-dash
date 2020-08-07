# test_loadcache.py

import unittest

from api.utils.loader import load, cache_source, read_cache

import pandas as pd

import os


class LoadCacheTest(unittest.TestCase):

    def setUp(self):
        loader = "gsheet"
        gsheet_url = 'https://docs.google.com/spreadsheets/d/11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do/edit#gid=1988095192'

        self.data = load(
            file_or_buffer=gsheet_url,
            loader=loader,
        )

        self.save = False

    
    def test_cache_source(self):
        assert self.data is not None