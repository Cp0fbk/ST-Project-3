# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest
import csv
import search_config as config

class SearchLevel2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(config.IMPLICIT_WAIT)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, config.EXPLICIT_WAIT)
        
    def test_search_all_test_cases(self):
        """Execute all search test cases from CSV"""
        with open(config.TEST_DATA_FILE, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                with self.subTest(tc_id=row['TC_ID']):
                    self._run_search_test(row)
    
    def _run_search_test(self, test_data):
        """Execute single search test case"""
        tc_id = test_data['TC_ID']
        search_term = test_data['Search_Term']
        expected_result = test_data['Expected_Results']
        expected_count = int(test_data['Expected_Count'])
        
        print(f"\n{'='*60}")
        print(f"TC ID: {tc_id}")
        print(f"Search Term: {search_term}")
        print(f"Expected: {expected_result} ({expected_count} items)")
        print(f"{'='*60}")
        
        try:
            # Step 1: Navigate to homepage
            self._navigate_to_home()
            
            # Step 2: Perform search
            self._perform_search(search_term)
            
            # Step 3: Verify results
            self._verify_search_results(tc_id, expected_result, expected_count)
            
            print(f"✓ {tc_id}: PASSED")
            
        except AssertionError as e:
            print(f"✗ {tc_id}: FAILED - {str(e)}")
            raise
        except Exception as e:
            print(f"✗ {tc_id}: ERROR - {str(e)}")
            raise
    
    def _navigate_to_home(self):
        """Navigate to homepage"""
        self.driver.get(config.BASE_URL)
        self.wait.until(EC.presence_of_element_located(config.SEARCH_INPUT))
    
    def _perform_search(self, search_term):
        """Enter search term and submit"""
        search_box = self.driver.find_element(*config.SEARCH_INPUT)
        search_box.clear()
        search_box.send_keys(search_term)
        
        search_button = self.driver.find_element(*config.SEARCH_BUTTON)
        search_button.click()
        
        # Wait for results page
        self.wait.until(EC.presence_of_element_located(config.PRODUCT_CONTAINER))
    
    def _verify_search_results(self, tc_id, expected_result, expected_count):
        """Verify search results match expectations"""
        if expected_count == 0:
            self._verify_no_products(tc_id)
        else:
            self._verify_products_found(tc_id, expected_result, expected_count)
    
    def _verify_no_products(self, tc_id):
        """Verify no products message is displayed"""
        try:
            no_product_element = self.driver.find_element(*config.NO_PRODUCT_MSG)
            self.assertIsNotNone(no_product_element)
            print(f"  → No products found (as expected)")
        except NoSuchElementException:
            self.fail(f"{tc_id}: Expected 'no product' message not found")
    
    def _verify_products_found(self, tc_id, expected_result, expected_count):
        """Verify correct products are displayed"""
        # Get all product titles
        product_elements = self.driver.find_elements(*config.PRODUCT_TITLES)
        actual_count = len(product_elements)
        
        # Verify count
        self.assertEqual(actual_count, expected_count,
                        f"Expected {expected_count} products, found {actual_count}")
        print(f"  → Found {actual_count} products")
        
        # Verify product names
        for idx, product in enumerate(product_elements, 1):
            product_name = product.text
            self.assertIn(expected_result.lower(), product_name.lower(),
                         f"Product '{product_name}' doesn't contain '{expected_result}'")
            print(f"  → Product {idx}: {product_name}")
        
        # Verify result info text
        try:
            result_info = self.driver.find_element(*config.RESULT_INFO)
            print(f"  → Result info: {result_info.text}")
        except NoSuchElementException:
            pass
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print(f"\n{'='*60}")
        print("All search tests completed")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    unittest.main(verbosity=2)