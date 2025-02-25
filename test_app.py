import unittest
from tax_app import calculate_tax_new, calculate_tax_old, show_tax_app
from forecast import extract_tax_data_from_pdf, show_forecast
from tax_advice import show_tax_advice
import pandas as pd
import fitz  # PyMuPDF

class TestTaxApp(unittest.TestCase):

    def test_calculate_tax_new(self):
        # Test if the function returns a float
        result = calculate_tax_new(500000)
        self.assertIsInstance(result, float)

    def test_calculate_tax_old(self):
        # Test if the function returns a float
        result = calculate_tax_old(1000000, 200000)
        self.assertIsInstance(result, float)

    def test_extract_tax_data_from_pdf(self):
        # Test if the function returns a DataFrame
        pdf_path = "time_series.pdf"
        df = extract_tax_data_from_pdf(pdf_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("Year", df.columns)
        self.assertIn("Total Taxes (Rs. crore)", df.columns)

    def test_show_tax_app(self):
        # Test if the function can be called without errors
        try:
            show_tax_app()
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result)

    def test_show_forecast(self):
        # Test if the function can be called without errors
        try:
            show_forecast()
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result)

    def test_show_tax_advice(self):
        # Test if the function can be called without errors
        try:
            show_tax_advice()
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()