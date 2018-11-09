import unittest
import pandas as pd
from FWF import FWF as fwf


class FWFTestCase(unittest.TestCase):
    """Tests for `test_FWF.py`."""

    def create_dataframe(self):
        data = {'Name': ['Tom', 'Jack', 'Steve',
                         'Ricky'], 'Age': [28, 34, 29, 42]}
        df = pd.DataFrame(data)
        return df

    def get_config(self):
        CONFIG = {
            'Age': {
                'required': True,
                'start_pos': 1,
                'end_pos': 3,
                'alignment': 'left',
                'padding': ' '
            },

            'Name': {
                'required': True,
                'start_pos': 4,
                'end_pos': 8,
                'alignment': 'left',
                'padding': ' '
            },
        }
        return CONFIG

    def test_dataframe_created(self):
        df = self.create_dataframe()
        self.assertTrue(df is not None)

    def test_config_created(self):
        config = self.get_config()
        self.assertTrue(config is not None)

    def test_FWF_created(self):
        config = self.get_config()
        df = self.create_dataframe()
        fw = fwf(config, df)
        self.assertTrue(fw is not None)

    def test_FWF_string(self):
        config = self.get_config()
        df = self.create_dataframe()
        fw = fwf(config, df)
        stroutput = fw.to_fwf()
        self.assertTrue(stroutput is not None)

    def test_FWF_string_linecount(self):
        config = self.get_config()
        df = self.create_dataframe()
        fw = fwf(config, df)
        stroutput = fw.to_fwf()
        nlines = len(stroutput.splitlines())
        self.assertTrue(nlines > 3)


if __name__ == '__main__':
    unittest.main()
