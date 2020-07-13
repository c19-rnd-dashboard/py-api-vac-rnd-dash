# ghseetloader.py
import pandas as pd


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
        



def load_gsheet(url:str=None, dtype='csv', key=None, sheet=None) -> pd.DataFrame:
    gs = DataSourceProtocol()
    url = gs.gen_url(dtype=dtype, key=key, sheet=sheet)


