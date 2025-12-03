# -*- coding: utf-8 -*-
"""
Level 1: Data-driven testing approach
Tests are driven by data from CSV file
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest
import csv
import time
import re
import os
from ddt import ddt, data, unpack


def load_test_data():
    """Load test data from CSV file"""
    test_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'price_filter_test_data.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        test_data = list(csv_reader)
    
    return test_data


@ddt
class DataDrivenPriceFilterTest(unittest.TestCase):
    
    def setUp(self):
        """Set up for each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://ecommerce-playground.lambdatest.io/"
        self.verificationErrors = []
        self.wait = WebDriverWait(self.driver, 10)
    
    @data(*load_test_data())
    def test_price_filter(self, test_case):
        """Test price filter with data from CSV - runs once per test case"""
        
        print(f"\n{'='*60}")
        print(f"Running: {test_case['test_case_id']}")
        print(f"Description: {test_case['test_description']}")
        print(f"Min Price: {test_case['min_price']}, Max Price: {test_case['max_price']}")
        print(f"{'='*60}")
        
        try:
            # Navigate to the website
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Click search button
            search_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            search_btn.click()
            time.sleep(2)
            
            # Enter minimum price
            min_price_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='mz-filter-panel-0-0']/div/div[2]/input")
                )
            )
            min_price_field.clear()
            if test_case['min_price']:
                min_price_field.send_keys(test_case['min_price'])
            
            # Enter maximum price
            max_price_field = self.driver.find_element(
                By.XPATH, "//div[@id='mz-filter-panel-0-0']/div/div[2]/input[2]"
            )
            max_price_field.clear()
            if test_case['max_price']:
                max_price_field.send_keys(test_case['max_price'])
            
            # Apply filter
            max_price_field.send_keys(Keys.ENTER)
            time.sleep(3)
            
            # Verify results based on expected outcome
            if test_case['expected_result'] == 'pass':
                # Verify product price is displayed
                product_price = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/div/div/div/div[2]/div/span"
                ).text
                print(f"✓ Product price found: {product_price}")
                
                # Verify price format
                self.assertRegex(product_price, r'^\$\d+\.\d{2}$', 
                               f"Price format invalid: {product_price}")
                print(f"✓ Price format is valid")
                
                # Verify pagination if expected
                if test_case['expected_pagination'] != 'N/A':
                    pagination = self.driver.find_element(
                        By.XPATH, "//div[@id='entry_212470']/div/div[2]"
                    ).text
                    print(f"✓ Pagination: {pagination}")
                
                print(f"✓ Test Case {test_case['test_case_id']} PASSED")
            
            else:  # expected_result == 'fail'
                # For negative test cases, we expect no valid results or error handling
                if test_case['expected_pagination'] == 'N/A':
                    # Check for "No products found" message
                    not_found_message = self.driver.find_element(
                        By.XPATH, "//div[@id='entry_212469']/p"
                    ).text
                    self.assertEqual(
                        not_found_message,
                        "There is no product that matches the search criteria.",
                        f"Expected 'No products found' message, but got: {not_found_message}"
                    )
                    print(f"✓ Correct 'No products found' message displayed")
                print(f"✓ Test Case {test_case['test_case_id']} PASSED (Negative test)")
        
        except Exception as e:
            print(f"✗ Test Case {test_case['test_case_id']} encountered error: {str(e)}")
            # Re-raise for unittest to catch
            raise
    
    def tearDown(self):
        """Clean up after each test"""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)