from utils.load import store_data
import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from main import main
import pandas as pd
 
class TestLoad(TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {"Title":['LOlzzz'], "Rating":[4.3], 
             "Number_Color":[5], "Size":['M'], 
             "Gender":['L'], "Timestamp":['2025-05-07 02:30:46.036413+07'], 
             "Price_in_dollars":[23.30], "Price_in_rupiah":[150000]}
        )
        self.db_url = 'postgresql+psycopg2://developer:developer@localhost:5432/fashionst'
        self.tablename = 'unittest'
        self.schema = 'testing'
    
    def test_store_data(self):
        store_data(self.data, self.db_url, self.tablename, self.schema)

    @staticmethod   
    @patch('utils.load.create_engine')
    @patch("main.store_data", side_effect=Exception(""))
    def test_db_error(self, mock_create_engine):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with("Terjadi kesalahan dalam proses: ")

    def tearDown(self):
        self.data = None
        
if __name__ == "__main__":
    unittest.main()