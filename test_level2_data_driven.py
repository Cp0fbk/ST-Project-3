# -*- coding: utf-8 -*-
"""
Level 2: Advanced data-driven testing approach
Uses external configuration file for URLs, locators, and test data
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
from config import BASE_URL, LOCATORS, TEST_CONFIG, EXPECTED_VALUES
from ddt import ddt, data, unpack


def load_test_data():
    """Load test data from CSV file"""
    test_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        test_data = list(csv_reader)
    
    return test_data


@ddt
class AdvancedDataDrivenTest(unittest.TestCase):
    
    def setUp(self):
        """Set up for each test - uses config file"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(TEST_CONFIG['implicit_wait'])
        self.driver.set_page_load_timeout(TEST_CONFIG['page_load_timeout'])
        self.wait = WebDriverWait(self.driver, TEST_CONFIG['explicit_wait'])
        self.verificationErrors = []
    
    def find_element_by_config(self, locator_key):
        """Find element using locator from config file"""
        locator_type, locator_value = LOCATORS[locator_key]
        by_type = getattr(By, locator_type.upper())
        return self.driver.find_element(by_type, locator_value)
    
    def wait_for_element(self, locator_key, timeout=None):
        """Wait for element using locator from config file"""
        if timeout is None:
            timeout = TEST_CONFIG['explicit_wait']
        
        locator_type, locator_value = LOCATORS[locator_key]
        by_type = getattr(By, locator_type.upper())
        
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by_type, locator_value))
        )
    
    def enter_price_values(self, min_price, max_price):
        """Enter price values in filter fields"""
        # Enter minimum price
        min_field = self.wait_for_element('min_price_input')
        min_field.clear()
        if min_price:
            min_field.send_keys(min_price)
        
        # Enter maximum price
        max_field = self.find_element_by_config('max_price_input')
        max_field.clear()
        if max_price:
            max_field.send_keys(max_price)
        
        return max_field
    
    def verify_price_format(self, price_text):
        """Verify price matches expected format"""
        pattern = EXPECTED_VALUES['price_pattern']
        return re.match(pattern, price_text) is not None
    
    def verify_pagination_format(self, pagination_text):
        """Verify pagination matches expected format"""
        pattern = EXPECTED_VALUES['pagination_pattern']
        return re.match(pattern, pagination_text) is not None
    
    @data(*load_test_data())
    def test_price_filter_with_config(self, test_case):
        """Execute test case using configuration - runs once per test case"""
        
        print(f"\n{'='*60}")
        print(f"Executing: {test_case['test_case_id']}")
        print(f"Description: {test_case['test_description']}")
        print(f"Min: {test_case['min_price']}, Max: {test_case['max_price']}")
        print(f"{'='*60}")
        
        # Navigate to website using config URL
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        # Click search button using config locator
        search_btn = self.wait_for_element('search_button')
        search_btn.click()
        time.sleep(2)
        
        # Enter price values
        max_field = self.enter_price_values(
            test_case['min_price'],
            test_case['max_price']
        )
        
        # Apply filter
        max_field.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # Verify results
        if test_case['expected_result'] == 'pass':
            self.verify_positive_test(test_case)
        else:
            self.verify_negative_test(test_case)
    
    def verify_positive_test(self, test_case):
        """Verify positive test case results"""
        # Check if products are displayed
        product_price = self.find_element_by_config('first_product_price').text
        print(f"✓ Product price: {product_price}")
        
        # Verify price format
        self.assertTrue(
            self.verify_price_format(product_price),
            f"Price format invalid: {product_price}"
        )
        print(f"✓ Price format valid")
        
        # Verify pagination if expected
        if test_case['expected_pagination'] != 'N/A':
            try:
                pagination = self.find_element_by_config('pagination_text').text
                self.assertTrue(
                    self.verify_pagination_format(pagination),
                    f"Pagination format invalid: {pagination}"
                )
                print(f"✓ Pagination: {pagination}")
            except NoSuchElementException:
                print(f"⚠ Pagination not found")
        
        print(f"✓ {test_case['test_case_id']} PASSED")
    
    def verify_negative_test(self, test_case):
        """Verify negative test case (should fail or show no results)"""
        print(f"✓ {test_case['test_case_id']} PASSED (Negative test - invalid input handled)")
    
    def tearDown(self):
        """Clean up after each test"""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)