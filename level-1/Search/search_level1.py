# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import csv

class SearchLevel1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.base_url = "https://ecommerce-playground.lambdatest.io/"
        
    def test_search_functionality(self):
        """Test search with multiple terms from CSV"""
        with open('search_test_data.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                with self.subTest(tc_id=row['TC_ID']):
                    self._execute_search_test(row)
    
    def _execute_search_test(self, test_data):
        driver = self.driver
        tc_id = test_data['TC_ID']
        search_term = test_data['Search_Term']
        expected_result = test_data['Expected_Results']
        expected_count = int(test_data['Expected_Count'])
        
        print(f"\nExecuting {tc_id}: Searching for '{search_term}'")
        
        # Navigate to home page
        driver.get(self.base_url)
        
        # Search
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys(search_term)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "product-search"))
        )
        
        # Verify results
        if expected_count == 0:
            # No products expected
            try:
                no_product_msg = driver.find_element(By.XPATH, "//p[contains(text(),'no product')]")
                self.assertIsNotNone(no_product_msg)
                print(f"{tc_id}: PASSED - No products found as expected")
            except:
                self.fail(f"{tc_id}: FAILED - Expected no products")
        else:
            # Products expected
            products = driver.find_elements(By.XPATH, "//h4[@class='title']/a")
            actual_count = len(products)
            
            self.assertEqual(actual_count, expected_count, 
                           f"{tc_id}: Expected {expected_count} products, found {actual_count}")
            
            # Verify product names contain expected result
            for product in products:
                product_name = product.text
                self.assertIn(expected_result.lower(), product_name.lower(),
                            f"{tc_id}: Product '{product_name}' doesn't contain '{expected_result}'")
            
            print(f"{tc_id}: PASSED - Found {actual_count} products")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)