import unittest
import os
from extractor import search

class TestIUPACTermExtractor(unittest.TestCase):
    # Set up necessary files and data for testing
    def setUp(self):
        # Create a sample JSON file for testing
        self.json_file = 'test_iupac_terms.json'
        with open(self.json_file, 'w') as file:
            file.write('{"terms": {"list": {"term1": {"title": "term1", "status": "active", "url": "https://example.com"}}}}')

        # Define terms for extraction
        self.terms_to_extract = ['term1']

        # Define output CSV file
        self.output_csv_file = 'test_extracted_terms.csv'

    # Test the search function with valid data
    def test_search_valid_data(self):
        search(self.terms_to_extract, self.json_file, self.output_csv_file)
        self.assertTrue(os.path.exists(self.output_csv_file))  # Check if the CSV file was created

        # Check the content of the generated CSV file
        with open(self.output_csv_file, 'r') as file:
            csv_data = file.read()
            self.assertIn('term1', csv_data)  # Check if the extracted term is present in the CSV

    # Test the search function with invalid JSON file
    def test_search_invalid_json_file(self):
        invalid_json_file = 'nonexistent_file.json'
        with self.assertRaises(FileNotFoundError):
            search(self.terms_to_extract, invalid_json_file, self.output_csv_file)

    # Clean up after testing
    def tearDown(self):
        # Remove temporary files created during testing
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        if os.path.exists(self.output_csv_file):
            os.remove(self.output_csv_file)

if __name__ == '__main__':
    unittest.main()
