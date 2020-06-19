import unittest

import pandas as pd

from api.utils.tools import coalesce


class ToolTest(unittest.TestCase):
    
    def test_coalesce(self):
        self.assertIsNone(coalesce(None, None))
        self.assertEqual('val', coalesce(None, 'val'))
        self.assertEqual('val', coalesce('val', None))