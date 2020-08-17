# test_loadcache.py

import unittest

from api.utils.loader import (
    load, cache_source, check_cache, read_cache, clear_cache,
)

from api.utils.loader.loaders import FileLoader

import pandas as pd

import os

import logging 
import json

tlog = logging.getLogger(__name__)


class LoadCacheTest(unittest.TestCase):

    def setUp(self):
        self.loader = "gsheet"
        self.gsheet_url = 'https://docs.google.com/spreadsheets/d/11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do/edit#gid=1988095192'

        self.save = False
        self.savereadpath = 'CacheRead.txt'


    def tearDown(self):
        clear_cache()


    def test_cache_source(self):
        loader = FileLoader(
            filename=self.gsheet_url,
            loader=self.loader,
            cache=False,
        )
        data = loader.fetch_transform()
        cache_source(loader)


    def test_cache_read(self):
        loader = FileLoader(
            filename=self.gsheet_url,
            loader=self.loader,
            cache=False,
        )
        data = loader.fetch_transform()
        cache_source(loader)

        read = read_cache(loader)
        self.assertIsNotNone(read)

        # tlog.info(f'CacheRead: {read}')  
        # tlog.info(f'Read Type: {type(read)}')
        # tlog.info(f'Dir read: {dir(read)}')

        if self.save:
            with open(self.savereadpath, 'w') as f:
                f.write(read.to_csv())
