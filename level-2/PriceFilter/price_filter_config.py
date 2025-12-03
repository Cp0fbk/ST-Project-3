# -*- coding: utf-8 -*-
"""
Configuration file for test data and element locators
Level 2: Data-driven testing with externalized test data and element locators
"""

# Site URLs
BASE_URL = "https://ecommerce-playground.lambdatest.io/"
SEARCH_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=product/search"

# Element Locators
LOCATORS = {
    # Search and Filter Elements
    "search_button": ("xpath", "//button[@type='submit']"),
    "min_price_input": ("xpath", "//div[@id='mz-filter-panel-0-0']/div/div[2]/input"),
    "max_price_input": ("xpath", "//div[@id='mz-filter-panel-0-0']/div/div[2]/input[2]"),
    
    # Product Elements
    "first_product_price": ("xpath", "//div[@id='entry_212469']/div/div/div/div[2]/div/span"),
    "second_product_price": ("xpath", "//div[@id='entry_212469']/div/div[2]/div/div[2]/div/span"),
    
    # Pagination Element
    "pagination_text": ("xpath", "//div[@id='entry_212470']/div/div[2]"),
    
    # No Product Found Message
    "no_product_message": ("xpath", "//div[@id='entry_212469']/p"),
    
    # Product List
    "product_list": ("xpath", "//div[contains(@class, 'product-layout')]"),
    "product_prices": ("xpath", "//span[@class='price-new'] | //span[@class='price-old']"),
    
    # Filter Panel
    "filter_panel": ("xpath", "//div[@id='mz-filter-panel-0-0']"),
    "apply_filter_button": ("xpath", "//button[contains(text(), 'Apply')]"),
    "clear_filter_button": ("xpath", "//button[contains(text(), 'Clear')]"),
}

# Test Configuration
TEST_CONFIG = {
    "implicit_wait": 30,
    "explicit_wait": 10,
    "page_load_timeout": 30,
    "browser": "chrome",
}

# Expected Values
EXPECTED_VALUES = {
    "currency_symbol": "$",
    "price_pattern": r"^\$\d{1,3}(,\d{3})*\.\d{2}$",
    "pagination_pattern": r"Showing \d+ to \d+ of \d+ \(\d+ Pages\)",
    "no_product_message": "There is no product that matches the search criteria.",
}