import unittest

import pandas as pd

from api.utils.transform import convert_to_datetime

import logging
import logging.config 

logging.config.fileConfig(fname='tests/testconfig.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)
logger.info(__name__)




class ToolTest(unittest.TestCase):
    
    def test_coalesce(self):
        self.assertIsNone(coalesce(None, None))
        self.assertEqual('val', coalesce(None, 'val'))
        self.assertEqual('val', coalesce('val', None))


if __name__ == "__main__":
    unittest.main()