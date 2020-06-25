import unittest

import pandas as pd

from api.utils.transform import convert_to_datetime
from tests.testconfig import get_logger


logger = get_logger(__name__)


class DateTimeConversionTest(unittest.TestCase):
    
    def setUp(self):
        self.sdate = '2020/02/02'
        self.sbaddates = ['2020/02/200', '202/12/20', '1990/10/35', '5/5/2045']

    def test_convert_to_datetime(self):
        nm = 'BasicConversion'
        result = convert_to_datetime(self.sdate)

        logger.info('-'.join([nm, str(result)]))
        self.assertEqual('2020', str(result.year))

    def test_catch_bad_date(self):
        nm = 'BadConversionDay: '


        for dst in self.sbaddates:
            result = convert_to_datetime(dst)
            logger.info(''.join([nm, str(result)]))
            self.assertIsNone(result)




if __name__ == "__main__":
    unittest.main()