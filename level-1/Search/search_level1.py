# -*- coding: utf-8 -*-
"""
Level 1: Data-driven testing approach
Tests are driven by data from CSV file
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest
import csv
import time
import os
from ddt import ddt, data, unpack


def load_test_data1():
    """Load test data from CSV file 1"""
    test_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'search_test_data1.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        test_data = list(csv_reader)
    
    return test_data


def load_test_data2():
    """Load test data from CSV file 2"""
    test_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'search_test_data2.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        test_data = list(csv_reader)
    
    return test_data


@ddt
class SearchLevel1(unittest.TestCase):
    
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
        print("Starting Level 1 Search Test Execution")
        print("="*60)
    
    def setUp(self):
        """Set up for each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "https://ecommerce-playground.lambdatest.io/"
        self.verificationErrors = []
        self.wait = WebDriverWait(self.driver, 10)
        self.current_test_id = None
    
    @data(*load_test_data1())
    def test_search_single_term(self, test_case):
        """Test search functionality with single search term from CSV"""
        
        self.current_test_id = test_case['TC_ID']
        SearchLevel1.total_tests += 1
        
        print(f"\n{'='*60}")
        print(f"Running: {test_case['TC_ID']}")
        print(f"Description: {test_case['Description']}")
        print(f"Search Term: '{test_case['Search_Term']}'")
        print(f"{'='*60}")
        
        try:
            # Navigate to home page
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Enter search term
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "search"))
            )
            search_box.clear()
            search_box.send_keys(test_case['Search_Term'])
            
            # Click search button
            search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            search_button.click()
            time.sleep(3)
            
            # Wait for results page
            self.wait.until(
                EC.presence_of_element_located((By.ID, "product-search"))
            )
            
            # Check what's actually displayed
            product_found = False
            not_found_found = False
            count_info_found = False
            
            actual_product_name = None
            actual_not_found_msg = None
            actual_count_info = None
            
            # Try to find product name
            try:
                product_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/div/div[2]/div/div[2]/h4/a"
                )
                actual_product_name = product_element.text
                product_found = True
            except NoSuchElementException:
                pass
            
            # Try to find "not found" message
            try:
                not_found_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/p"
                )
                actual_not_found_msg = not_found_element.text
                not_found_found = True
            except NoSuchElementException:
                pass
            
            # Try to find count information
            try:
                count_info_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212470']/div/div[2]"
                )
                actual_count_info = count_info_element.text
                count_info_found = True
            except NoSuchElementException:
                pass
            
            # Verify Expected_Results
            if test_case['Expected_Results'] != 'N/A':
                if not product_found:
                    self.fail(f"Expected product '{test_case['Expected_Results']}', but no product found")
                
                # Check if product name contains expected result
                self.assertIn(test_case['Expected_Results'].lower(), actual_product_name.lower(),
                            f"Expected product containing '{test_case['Expected_Results']}', but got '{actual_product_name}'")
                print(f"✓ Product found: {actual_product_name}")
            else:
                if product_found:
                    self.fail(f"Expected no product (N/A), but found: {actual_product_name}")
            
            # Verify Expected_NotFound
            if test_case['Expected_NotFound'] != 'N/A':
                if not not_found_found:
                    self.fail(f"Expected 'not found' message '{test_case['Expected_NotFound']}', but no message found")
                
                self.assertEqual(actual_not_found_msg, test_case['Expected_NotFound'],
                               f"Expected message '{test_case['Expected_NotFound']}', but got '{actual_not_found_msg}'")
                print(f"✓ 'Not found' message matches: {actual_not_found_msg}")
            else:
                if not_found_found:
                    self.fail(f"Expected no 'not found' message (N/A), but found: {actual_not_found_msg}")
            
            # Verify Expected_Count
            if test_case['Expected_Count'] != 'N/A':
                if not count_info_found:
                    self.fail(f"Expected count info '{test_case['Expected_Count']}', but count element not found")
                
                self.assertEqual(actual_count_info, test_case['Expected_Count'],
                               f"Expected count info '{test_case['Expected_Count']}', but got '{actual_count_info}'")
                print(f"✓ Count info matches: {actual_count_info}")
            else:
                if count_info_found:
                    self.fail(f"Expected no count info (N/A), but found: {actual_count_info}")
            
            print(f"✓ Test Case {test_case['TC_ID']} PASSED")
            
            # Record success
            SearchLevel1.test_results['passed'].append(self.current_test_id)
        
        except AssertionError as e:
            print(f"✗ Test Case {test_case['TC_ID']} FAILED: {str(e)}")
            SearchLevel1.test_results['failed'].append({
                'test_id': self.current_test_id,
                'reason': str(e)
            })
            raise
        
        except Exception as e:
            print(f"✗ Test Case {test_case['TC_ID']} ERROR: {str(e)}")
            SearchLevel1.test_results['errors'].append({
                'test_id': self.current_test_id,
                'reason': str(e)
            })
            raise
    
    @data(*load_test_data2())
    def test_search_two_terms(self, test_case):
        """Test search functionality with two consecutive search terms from CSV"""
        
        self.current_test_id = test_case['TC_ID']
        SearchLevel1.total_tests += 1
        
        print(f"\n{'='*60}")
        print(f"Running: {test_case['TC_ID']}")
        print(f"Description: {test_case['Description']}")
        print(f"Search Term 1: '{test_case['Search_Term1']}'")
        print(f"Search Term 2: '{test_case['Search_Term2']}'")
        print(f"{'='*60}")
        
        try:
            # ========== FIRST SEARCH ==========
            print(f"\n--- First Search: '{test_case['Search_Term1']}' ---")
            
            # Navigate to home page
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Enter first search term
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "search"))
            )
            search_box.clear()
            search_box.send_keys(test_case['Search_Term1'])
            
            # Click search button
            search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            search_button.click()
            time.sleep(3)
            
            # Wait for results page
            self.wait.until(
                EC.presence_of_element_located((By.ID, "product-search"))
            )
            
            # Check first search results
            product_found = False
            count_info_found = False
            actual_product_name = None
            actual_count_info = None
            
            # Try to find product name
            try:
                product_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/div/div[2]/div/div[2]/h4/a"
                )
                actual_product_name = product_element.text
                product_found = True
            except NoSuchElementException:
                pass
            
            # Try to find count information
            try:
                count_info_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212470']/div/div[2]"
                )
                actual_count_info = count_info_element.text
                count_info_found = True
            except NoSuchElementException:
                pass
            
            # Verify Expected_Results1
            if test_case['Expected_Results1'] != 'N/A':
                if not product_found:
                    self.fail(f"First search: Expected product '{test_case['Expected_Results1']}', but no product found")
                
                self.assertIn(test_case['Expected_Results1'].lower(), actual_product_name.lower(),
                            f"First search: Expected product containing '{test_case['Expected_Results1']}', but got '{actual_product_name}'")
                print(f"✓ First search - Product found: {actual_product_name}")
            else:
                if product_found:
                    self.fail(f"First search: Expected no product (N/A), but found: {actual_product_name}")
            
            # Verify Expected_Count1
            if test_case['Expected_Count1'] != 'N/A':
                if not count_info_found:
                    self.fail(f"First search: Expected count info '{test_case['Expected_Count1']}', but count element not found")
                
                self.assertEqual(actual_count_info, test_case['Expected_Count1'],
                               f"First search: Expected count info '{test_case['Expected_Count1']}', but got '{actual_count_info}'")
                print(f"✓ First search - Count info matches: {actual_count_info}")
            else:
                if count_info_found:
                    self.fail(f"First search: Expected no count info (N/A), but found: {actual_count_info}")
            
            # ========== SECOND SEARCH ==========
            print(f"\n--- Second Search: '{test_case['Search_Term2']}' ---")
            
            # Enter second search term (reuse search box on results page)
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "search"))
            )
            search_box.clear()
            search_box.send_keys(test_case['Search_Term2'])
            
            # Click search button
            search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            search_button.click()
            time.sleep(3)
            
            # Wait for results page
            self.wait.until(
                EC.presence_of_element_located((By.ID, "product-search"))
            )
            
            # Check second search results
            product_found = False
            count_info_found = False
            actual_product_name = None
            actual_count_info = None
            
            # Try to find product name
            try:
                product_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212469']/div/div[2]/div/div[2]/h4/a"
                )
                actual_product_name = product_element.text
                product_found = True
            except NoSuchElementException:
                pass
            
            # Try to find count information
            try:
                count_info_element = self.driver.find_element(
                    By.XPATH, "//div[@id='entry_212470']/div/div[2]"
                )
                actual_count_info = count_info_element.text
                count_info_found = True
            except NoSuchElementException:
                pass
            
            # Verify Expected_Results2
            if test_case['Expected_Results2'] != 'N/A':
                if not product_found:
                    self.fail(f"Second search: Expected product '{test_case['Expected_Results2']}', but no product found")
                
                self.assertIn(test_case['Expected_Results2'].lower(), actual_product_name.lower(),
                            f"Second search: Expected product containing '{test_case['Expected_Results2']}', but got '{actual_product_name}'")
                print(f"✓ Second search - Product found: {actual_product_name}")
            else:
                if product_found:
                    self.fail(f"Second search: Expected no product (N/A), but found: {actual_product_name}")
            
            # Verify Expected_Count2
            if test_case['Expected_Count2'] != 'N/A':
                if not count_info_found:
                    self.fail(f"Second search: Expected count info '{test_case['Expected_Count2']}', but count element not found")
                
                self.assertEqual(actual_count_info, test_case['Expected_Count2'],
                               f"Second search: Expected count info '{test_case['Expected_Count2']}', but got '{actual_count_info}'")
                print(f"✓ Second search - Count info matches: {actual_count_info}")
            else:
                if count_info_found:
                    self.fail(f"Second search: Expected no count info (N/A), but found: {actual_count_info}")
            
            print(f"\n✓ Test Case {test_case['TC_ID']} PASSED")
            
            # Record success
            SearchLevel1.test_results['passed'].append(self.current_test_id)
        
        except AssertionError as e:
            print(f"✗ Test Case {test_case['TC_ID']} FAILED: {str(e)}")
            SearchLevel1.test_results['failed'].append({
                'test_id': self.current_test_id,
                'reason': str(e)
            })
            raise
        
        except Exception as e:
            print(f"✗ Test Case {test_case['TC_ID']} ERROR: {str(e)}")
            SearchLevel1.test_results['errors'].append({
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
        print("TEST EXECUTION SUMMARY - LEVEL 1 SEARCH")
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