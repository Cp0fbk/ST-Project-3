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
    # csv_path = os.path.join(os.path.dirname(__file__), 'test.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        test_data = list(csv_reader)
    
    return test_data


@ddt
class PriceFilterLevel1(unittest.TestCase):
    
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
        print("Starting Level 1 Test Execution")
        print("="*60)
    
    def setUp(self):
        """Set up for each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(15)
        self.base_url = "https://ecommerce-playground.lambdatest.io/"
        self.verificationErrors = []
        self.wait = WebDriverWait(self.driver, 10)
        self.current_test_id = None
    
    @data(*load_test_data())
    def test_price_filter(self, test_case):
        """Test price filter with data from CSV - runs once per test case"""
        
        self.current_test_id = test_case['test_case_id']
        PriceFilterLevel1.total_tests += 1
        
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
            
            # Check what's actually displayed
            product_price_found = False
            pagination_found = False
            not_found_found = False
            
            actual_price = None
            actual_pagination = None
            actual_not_found = None
            
            # Try to find product price
            try:
                actual_price = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/div/div/div/div[2]/div/span"
                ).text
                product_price_found = True
            except NoSuchElementException:
                pass
            
            # Try to find pagination
            try:
                actual_pagination = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212470']/div/div[2]"
                ).text
                pagination_found = True
            except NoSuchElementException:
                pass
            
            # Try to find "not found" message
            try:
                actual_not_found = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/p"
                ).text
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
                self.assertRegex(actual_price, r'^\$\d{1,3}(,\d{3})*\.\d{2}$', 
                            f"Price format invalid: {actual_price}")
                print(f" Price matches: {actual_price}")
            else:
                if product_price_found:
                    self.fail(f"Expected no product price (N/A), but found: {actual_price}")
            
            # Verify pagination
            if test_case['expected_pagination'] != 'N/A':
                if not pagination_found:
                    self.fail(f"Expected pagination '{test_case['expected_pagination']}', but no pagination found")
                
                self.assertEqual(actual_pagination, test_case['expected_pagination'],
                               f"Expected pagination '{test_case['expected_pagination']}', but got '{actual_pagination}'")
                print(f" Pagination matches: {actual_pagination}")
            else:
                if pagination_found:
                    self.fail(f"Expected no pagination (N/A), but found: {actual_pagination}")
            
            # Verify "not found" message
            if test_case['not_found'] != 'N/A':
                if not not_found_found:
                    self.fail(f"Expected 'not found' message '{test_case['not_found']}', but no message found")
                
                self.assertEqual(actual_not_found, test_case['not_found'],
                               f"Expected 'not found' message '{test_case['not_found']}', but got '{actual_not_found}'")
                print(f" 'Not found' message matches: {actual_not_found}")
            else:
                if not_found_found:
                    self.fail(f"Expected no 'not found' message (N/A), but found: {actual_not_found}")
            
            print(f" Test Case {test_case['test_case_id']} PASSED")
            
            # Record success
            PriceFilterLevel1.test_results['passed'].append(self.current_test_id)
        
        except AssertionError as e:
            print(f" Test Case {test_case['test_case_id']} FAILED: {str(e)}")
            PriceFilterLevel1.test_results['failed'].append({
                'test_id': self.current_test_id,
                'reason': str(e)
            })
            raise
        
        except Exception as e:
            print(f" Test Case {test_case['test_case_id']} ERROR: {str(e)}")
            PriceFilterLevel1.test_results['errors'].append({
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
        print("TEST EXECUTION SUMMARY - LEVEL 1")
        print("="*60)
        print(f"Total Tests: {cls.total_tests}")
        print(f"Passed: {len(cls.test_results['passed'])}")
        print(f"Failed: {len(cls.test_results['failed'])}")
        print(f"Errors: {len(cls.test_results['errors'])}")
        print("="*60)
    
        if cls.test_results['failed']:
            print("\n FAILED TEST CASES:")
            for failure in cls.test_results['failed']:
                print(f"  - {failure['test_id']}")
                print(f"    Reason: {failure['reason']}")
        
        if cls.test_results['errors']:
            print("\n ERROR TEST CASES:")
            for error in cls.test_results['errors']:
                print(f"  - {error['test_id']}")
                print(f"    Reason: {error['reason']}")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)