# -*- coding: utf-8 -*-
"""
Login config for Level 2 data-driven tests
"""
BASE_URL = "https://www.saucedemo.com/"

# element locators: (by_type, locator_value)
LOCATORS = {
    "username_field": ("id", "user-name"),
    "password_field": ("id", "password"),
    "login_button": ("id", "login-button"),
    "error_message": ("css", "h3[data-test='error']"),
    "inventory_page_marker": ("css", ".inventory_list"),
}

TEST_CONFIG = {
    "implicit_wait": 10,
    "explicit_wait": 10,
    "page_load_timeout": 30,
    "browser": "chrome",
}

EXPECTED_VALUES = {
    "username_required": "Epic sadface: Username is required",
    "password_required": "Epic sadface: Password is required",
    "invalid_credentials": "Username and password do not match any user in this service",
    "locked_out": "Epic sadface: Sorry, this user has been locked out.",
    "inventory_marker": "inventory_list"
}
