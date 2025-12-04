# -*- coding: utf-8 -*-
"""
Search Test Configuration File
Contains all URLs, locators, test data paths, and configuration settings
"""

from selenium.webdriver.common.by import By

# ========== BASE CONFIGURATION ==========
BASE_URL = "https://ecommerce-playground.lambdatest.io/"

# ========== TIMEOUT SETTINGS ==========
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# ========== LOCATORS ==========
# Using tuple format (By.TYPE, "locator_value") for consistency
SEARCH_INPUT = (By.NAME, "search")
SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
PRODUCT_CONTAINER = (By.ID, "product-search")
PRODUCT_TITLES = (By.XPATH, "//div[@id='entry_212469']/div/div[2]/div/div[2]/h4/a")
NO_PRODUCT_MSG = (By.XPATH, "//div[@id='entry_212469']/p")
RESULT_INFO = (By.XPATH, "//div[@id='entry_212470']/div/div[2]")

# ========== TEST DATA FILES ==========
TEST_DATA_FILE_1 = "search_test_data1.csv"
TEST_DATA_FILE_2 = "search_test_data2.csv"

# ========== EXPECTED VALUES ==========
EXPECTED_VALUES = {
    'no_product_message': 'There is no product that matches the search criteria.',
    'result_info_pattern': r'Showing \d+ to \d+ of \d+ \(\d+ Pages\)',
}

# ========== TEST CONFIGURATION ==========
TEST_CONFIG = {
    'implicit_wait': IMPLICIT_WAIT,
    'explicit_wait': EXPLICIT_WAIT,
    'page_load_timeout': PAGE_LOAD_TIMEOUT,
    'base_url': BASE_URL,
    'screenshot_on_failure': True,
    'screenshot_dir': 'screenshots',
}

# ========== VALIDATION SETTINGS ==========
VALIDATION = {
    'verify_product_name_contains': True,  # Check if product name contains expected text
    'case_sensitive': False,  # Case-insensitive comparison
    'verify_result_count': True,  # Verify result count information
    'verify_no_product_message': True,  # Verify "no product" message when applicable
}

# ========== WAIT TIMES (in seconds) ==========
WAIT_TIMES = {
    'after_navigation': 2,
    'after_search': 3,
    'after_click': 1,
}