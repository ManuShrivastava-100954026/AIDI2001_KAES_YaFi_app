import unittest
import json
import os
from utils import (
    get_stock_price,
    calculate_SMA,
    calculate_EMA,
    calculate_RSI,
    calculate_MACD,
    plot_stock_price,
    get_latest_news
)

class TestStockFunctions(unittest.TestCase):
    def setUp(self):
        self.valid_ticker = 'AAPL'  # Use a valid ticker symbol for testing
        self.invalid_ticker = 'INVALID'
        self.sma_window = 10
        self.ema_window = 10

    def test_get_stock_price(self):
        result = get_stock_price(self.valid_ticker)
        self.assertNotEqual(result, "No data available for this ticker.")
        self.assertTrue(result.replace('.', '', 1).isdigit(), "Price should be a number")

    def test_calculate_SMA(self):
        result = calculate_SMA(self.valid_ticker, self.sma_window)
        self.assertNotEqual(result, "No data available for this ticker.")
        self.assertTrue(result.replace('.', '', 1).isdigit(), "SMA should be a number")

    def test_calculate_EMA(self):
        result = calculate_EMA(self.valid_ticker, self.ema_window)
        self.assertNotEqual(result, "No data available for this ticker.")
        self.assertTrue(result.replace('.', '', 1).isdigit(), "EMA should be a number")

    def test_calculate_RSI(self):
        result = calculate_RSI(self.valid_ticker)
        self.assertNotEqual(result, "No data available for this ticker.")
        self.assertTrue(result.replace('.', '', 1).isdigit(), "RSI should be a number")

    def test_calculate_MACD(self):
        result = calculate_MACD(self.valid_ticker)
        self.assertNotEqual(result, "No data available for this ticker.")
        self.assertTrue(result.count(',') == 2, "MACD result should be comma-separated")

    def test_plot_stock_price(self):
        if not os.path.exists('static'):
            os.makedirs('static')
        result = plot_stock_price(self.valid_ticker)
        self.assertEqual(result, "Plot saved as stock.png")
        self.assertTrue(os.path.exists('static/stock.png'), "Plot image file should be created")

    def test_get_latest_news(self):
        result = get_latest_news(self.valid_ticker)
        news_list = json.loads(result)
        self.assertIsInstance(news_list, list)
        self.assertTrue(len(news_list) > 0, "There should be some news articles")
        self.assertTrue('Title' in news_list[0], "News should contain titles")

    def test_invalid_ticker(self):
        result = get_stock_price(self.invalid_ticker)
        self.assertEqual(result, "No data available for this ticker.")

if __name__ == '__main__':
    unittest.main()
