# ghseetloader.py
from .unfilteredcsv import load_unfiltered_csv

import pandas as pd
import re
import logging

tlog = logging.getLogger(__name__)


class DataSourceProtocol():
    """
    This class contains Google Datasource Protocol specifications to get data from google sheet.

    Built from https://stackoverflow.com/questions/33713084/download-link-for-google-spreadsheets-csv-export-with-multiple-sheets
    """

    def __init__(self, sourceurl=None, key=None):
        if sourceurl is not None:
            raise NotImplementedError('Key parsing from URL not implented. Manually strip doc key')

        self.sourceurl = sourceurl
        self.key = key
        self.GSHEET_BASE_URL = 'https://docs.google.com/spreadsheets/d'


    def _create_protocol_url(self, dtype, key=None, sheet=None):
        if key is None:
            key = self.key
        base_url = f'{self.GSHEET_BASE_URL}/{key}/export?format={dtype}&id={key}&gid={sheet}'
        return base_url


    def gen_url(self, *args, **kwargs):
        return self._create_protocol_url(*args, **kwargs)
        


def _parse_url(url):
# https://docs.google.com/spreadsheets/d/11FlafRMeQ2D6doEX_CMHyW4OqnXkp1FfrkLdsxhd0do/edit#gid=1988095192
    assert 'edit' in url, 'Edit URL not sent.  Is this preformatted?'
    pat = r'^.*\/d\/(.*)\/edit.*$'
    match = re.search(pat, url)
    return {
        'key':match.group(1),
        'sheet_id':url.split('=')[-1],
    }
    


def load_gsheet(url:str=None, dtype='csv', key=None, sheet=None, **kwargs) -> pd.DataFrame:
    tlog.info('Creating Gsheets protocol URL and sending to unfiltered csv.')
    gs = DataSourceProtocol()

    if url is not None:
        uparse = _parse_url(url)
        key = uparse['key']
        sheet = uparse['sheet_id']

    protocol_url =  gs.gen_url(dtype=dtype, key=key, sheet=sheet)

    return load_unfiltered_csv(protocol_url)



