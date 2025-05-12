import pandas as pd
import unittest
from unittest import TestCase, mock
from unittest.mock import patch
from utils.transform import transform_data

class TestTransform(TestCase):
    def setUp(self):
        self.data_dum = pd.DataFrame({
            'Title':['Hand Bag', 'Unknown Product', 'Waist Bag', 'Ransel Bag'],
            'Price': ['$23.00', 'Price Unavailable', '$45.30', '$31.10'],
            'Rating': ['4.3 / 5', '3.8', '2.7 / 5','Invalid Rating'],
            'Number_Color': ['5 Colors', '2 Colors', '4 Colors', '3 Colors'],
            'Size': ['Size: M', 'L', 'S', 'L'],
            'Gender': ['Female', 'Male', 'Gender: Female', 'Male']
        })
        self.exchange_rate = 16000
        
    def test_transform_data(self):
        result = transform_data(self.data_dum, self.exchange_rate)
        # Cek title
        self.assertIsInstance(result.loc[0, 'Title'], str)
        self.assertNotIsInstance(result.loc[0, 'Title'], int)
        # Cek harga
        
        self.assertEqual(result.loc[0, 'Price_in_dollars'], 23.00)
        self.assertEqual(result.loc[0, 'Price_in_rupiah'], int(result.loc[0, 'Price_in_dollars'] * self.exchange_rate))
        # Cek rating
        expected = 2.7
        self.assertIsInstance(result.loc[0, 'Rating'], float)
        self.assertEqual(result.loc[1, 'Rating'], expected)
        # Cek Number Color
        expected2 = [1, 2, 3, 4, 5]
        self.assertIn(result.loc[0, 'Number_Color'], expected2)
        self.assertIn(result.loc[1, 'Number_Color'], expected2)
        # Cek Size
        expected3 = ['S', 'M', 'L', 'XL']
        self.assertEqual(result.loc[0, 'Size'], expected3[1])
        self.assertEqual(result.loc[1, 'Size'], expected3[0])
        self.assertNotEqual(result.loc[1, 'Size'], expected3[3])
        # Cek Gender
        expected4 = ['Male', 'Female']
        self.assertNotEqual(result.loc[0, 'Gender'], expected4[0])
        self.assertNotEqual(result.loc[1, 'Gender'], expected4[0])
        # Cek tipe data
        self.assertEqual((result['Price'].dtype), float)
        self.assertEqual((result['Price_in_dollars'].dtype), float)
        self.assertEqual((result['Rating'].dtype), float)
        self.assertEqual((result['Number_Color'].dtype), int)
        # Cek kolom baru
        excepted_columns = result.columns
        self.assertIn('Price_in_dollars', excepted_columns)
        self.assertIn('Price_in_rupiah', excepted_columns)
        self.assertIn('Price', excepted_columns)
        
if __name__ == '__main__':
    unittest.main()
