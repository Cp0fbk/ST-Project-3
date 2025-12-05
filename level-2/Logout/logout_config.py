# -*- coding: utf-8 -*-
"""
Logout config for Level 2 data-driven tests
"""
BASE_URL = "https://www.saucedemo.com/"

LOCATORS = {
    "username_field": ("id", "user-name"),
    "password_field": ("id", "password"),
    "login_button": ("id", "login-button"),
    "menu_button": ("id", "react-burger-menu-btn"),
    "logout_button": ("id", "logout_sidebar_link"),
    "login_page_marker": ("css", ".login_container")
}

TEST_CONFIG = {
    "implicit_wait": 10,
    "explicit_wait": 10,
    "page_load_timeout": 30,
    "browser": "chrome",
}

EXPECTED_VALUES = {
    "logout_success": "https://www.saucedemo.com/",
    "inventory_marker": "inventory_list"
}
