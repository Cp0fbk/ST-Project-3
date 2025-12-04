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
import sys

# Add the current directory to the Python path to find config.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from price_filter_config import BASE_URL, LOCATORS, TEST_CONFIG, EXPECTED_VALUES
from ddt import ddt, data, unpack


def load_test_data():
    """Load test data from CSV file"""
    test_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'price_filter_test_data.csv')
    # csv_path = os.path.join(os.path.dirname(__file__), 'test.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        test_data = list(csv_reader)
    
    return test_data


@ddt
class PriceFilterLevel2(unittest.TestCase):
    
    # Class variables to track test results
    test_results = {
        'passed': [],
        'failed': [],
        'errors': []
    }
    total_tests = 0
    
    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        cls.test_results = {'passed': [], 'failed': [], 'errors': []}
        cls.total_tests = 0
        print("\n" + "="*60)
        print("Starting Level 2 Test Execution")
        print("="*60)
    
    def setUp(self):
        """Set up for each test - uses config file"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(TEST_CONFIG['implicit_wait'])
        self.driver.set_page_load_timeout(TEST_CONFIG['page_load_timeout'])
        self.wait = WebDriverWait(self.driver, TEST_CONFIG['explicit_wait'])
        self.verificationErrors = []
        self.current_test_id = None
    
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
        
        self.current_test_id = test_case['test_case_id']
        PriceFilterLevel2.total_tests += 1
        
        print(f"\n{'='*60}")
        print(f"Executing: {test_case['test_case_id']}")
        print(f"Description: {test_case['test_description']}")
        print(f"Min: {test_case['min_price']}, Max: {test_case['max_price']}")
        print(f"{'='*60}")
        
        try:
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
            
            # Check what's actually displayed
            product_price_found = False
            pagination_found = False
            not_found_found = False
            
            actual_price = None
            actual_pagination = None
            actual_not_found = None
            
            # Try to find product price
            try:
                actual_price = self.find_element_by_config('first_product_price').text
                product_price_found = True
            except NoSuchElementException:
                pass
            
            # Try to find pagination
            try:
                actual_pagination = self.find_element_by_config('pagination_text').text
                pagination_found = True
            except NoSuchElementException:
                pass
            
            # Try to find "not found" message
            try:
                actual_not_found = self.find_element_by_config('no_product_message').text
                not_found_found = True
            except NoSuchElementException:
                pass
            
            # Verify product price
            if test_case['expected_price'] != 'N/A':
                if not product_price_found:
                    self.fail(f"Expected price {test_case['expected_price']}, but no product price found")
                
                self.assertEqual(actual_price, test_case['expected_price'], 
                                f"Expected price {test_case['expected_price']}, but got {actual_price}")
                # Verify price format
                self.assertTrue(
                    self.verify_price_format(actual_price),
                    f"Price format invalid: {actual_price}"
                )
                print(f"✓ Price matches: {actual_price}")
            else:
                if product_price_found:
                    self.fail(f"Expected no product price (N/A), but found: {actual_price}")
            
            # Verify pagination
            if test_case['expected_pagination'] != 'N/A':
                if not pagination_found:
                    self.fail(f"Expected pagination '{test_case['expected_pagination']}', but no pagination found")
                
                self.assertEqual(actual_pagination, test_case['expected_pagination'],
                               f"Expected pagination '{test_case['expected_pagination']}', but got '{actual_pagination}'")
                # Verify pagination format
                self.assertTrue(
                    self.verify_pagination_format(actual_pagination),
                    f"Pagination format invalid: {actual_pagination}"
                )
                print(f"✓ Pagination matches: {actual_pagination}")
            else:
                if pagination_found:
                    self.fail(f"Expected no pagination (N/A), but found: {actual_pagination}")
            
            # Verify "not found" message
            if test_case['not_found'] != 'N/A':
                if not not_found_found:
                    self.fail(f"Expected 'not found' message '{test_case['not_found']}', but no message found")
                
                self.assertEqual(actual_not_found, test_case['not_found'],
                               f"Expected 'not found' message '{test_case['not_found']}', but got '{actual_not_found}'")
                print(f"✓ 'Not found' message matches: {actual_not_found}")
            else:
                if not_found_found:
                    self.fail(f"Expected no 'not found' message (N/A), but found: {actual_not_found}")
            
            print(f"✓ Test Case {test_case['test_case_id']} PASSED")
            
            # Record success
            PriceFilterLevel2.test_results['passed'].append(self.current_test_id)
        
        except AssertionError as e:
            print(f"✗ Test Case {test_case['test_case_id']} FAILED: {str(e)}")
            PriceFilterLevel2.test_results['failed'].append({
                'test_id': self.current_test_id,
                'reason': str(e)
            })
            raise
        
        except Exception as e:
            print(f"✗ Test Case {test_case['test_case_id']} ERROR: {str(e)}")
            PriceFilterLevel2.test_results['errors'].append({
                'test_id': self.current_test_id,
                'reason': str(e)
            })
            raise
    
    def tearDown(self):
        """Clean up after each test"""
        self.driver.quit()
    
    @classmethod
    def tearDownClass(cls):
        """Print summary after all tests"""
        print("\n" + "="*60)
        print("TEST EXECUTION SUMMARY - LEVEL 2")
        print("="*60)
        print(f"Total Tests: {cls.total_tests}")
        print(f"Passed: {len(cls.test_results['passed'])}")
        print(f"Failed: {len(cls.test_results['failed'])}")
        print(f"Errors: {len(cls.test_results['errors'])}")
        print("="*60)
        
        if cls.test_results['failed']:
            print("\n✗ FAILED TEST CASES:")
            for failure in cls.test_results['failed']:
                print(f"  - {failure['test_id']}")
                print(f"    Reason: {failure['reason']}")
        
        if cls.test_results['errors']:
            print("\n⚠ ERROR TEST CASES:")
            for error in cls.test_results['errors']:
                print(f"  - {error['test_id']}")
                print(f"    Reason: {error['reason']}")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)