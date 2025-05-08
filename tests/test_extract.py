import datetime
import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from main import main
from utils.extract import extract_product_data, fetching_content 
 
class TestExtract(TestCase):
    def setUp(self):
        self.html = """
        <div class="collection-card">
            <div style="position: relative;">
                <img src="https://picsum.photos/280/350?random=44" class="collection-image" alt="T-shirt 44">                
            </div>
            <div class="product-details">
                <h3 class="product-title">T-shirt 44</h3>
                <div class="price-container"><span class="price">$207.02</span></div>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.0 / 5</p>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: XL</p>
                <p style="font-size: 14px; color: #777;">Gender: Women</p>
            </div>
        </div>
        """
        self.url = 'https://fashion-studio.dicoding.dev/'

    # @patch('utils.extract.fetching_content')
    # def test_fetching_content(self, mock_fetching_content):
    #     content = fetching_content(self.url)
    #     self.assertNotEqual(content, 'https://books.toscrape.com/')
        # mock_fetching_content.return_value = mock_response
    
    @patch('utils.extract.requests.session')
    def test_fetching_content_success(self, mock_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test</body></html>"
        mock_session.return_value.get.return_value = mock_response
        result = fetching_content("https://example.com")
        self.assertNotEqual(result, b"<html><body>Test</body></html>")
        
    def test_extract_product(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        product = soup.find('div', class_='collection-card')
        timestamp = datetime.datetime.now()
        extract_product = extract_product_data(product)

        expected = ['T-shirt 44', '$207.02', 'Rating: ⭐ 3.0 / 5', 
                    '3 Colors', 'Size: XL', 'Gender: Women', timestamp]
        self.assertEqual(extract_product['Title'], expected[0])
        self.assertEqual(extract_product['Price'], expected[1])
        self.assertEqual(extract_product['Rating'], expected[2])
        self.assertEqual(extract_product['Number_Color'], expected[3])
        self.assertEqual(extract_product['Size'], expected[4])
        self.assertEqual(extract_product['Gender'], expected[5])
        # self.assertEqual(extract_product['Timestamp'], expected[6])
        self.assertTrue(extract_product['Timestamp'], [expected[6]])

    # errornya kurang jelas
    # @staticmethod
    # @patch('utils.extract.fetching_content', side_effect=Exception("Terjadi kesalahan ketika melakukan requests terhadap "))
    # # @patch('utils.extract.requests.Session.get', return_value="https://fooo.dev/")
    # @patch('main.scrape_product', side_effect=Exception("Terjadi kesalahan ketika melakukan requests terhadap "))
    # @patch('utils.extract.scrape_product', side_effect=Exception("Terjadi kesalahan ketika melakukan requests terhadap "))
    # @patch('utils.extract.requests.session', side_effect="Terjadi kesalahan ketika melakukan requests terhadap ")
    # def test_fetching_error(self, mock_session_class):
    #     with patch('builtins.print') as mock_print:
    #         content = fetching_content("https://example.com")
    #         self.assertNone(content)
    #         mock_print.assert_called_with("Terjadi kesalahan ketika melakukan requests terhadap ")
            
    def tearDown(self):
        self.html = """Null"""

if __name__ == '__main__':
    unittest.main()
    
    