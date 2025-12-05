# -*- coding: utf-8 -*-
"""
Level 2 Login tests (data-driven)
Uses external configuration file for URLs, locators, and CSV test data
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
import sys

# allow config import from same folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from login_config import BASE_URL, LOCATORS, TEST_CONFIG, EXPECTED_VALUES
from ddt import ddt, data

def load_test_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'login_test_data.csv')
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

@ddt
class LoginLevel2(unittest.TestCase):
    test_results = {'passed': [], 'failed': [], 'errors': []}
    total_tests = 0

    @classmethod
    def setUpClass(cls):
        cls.test_results = {'passed': [], 'failed': [], 'errors': []}
        cls.total_tests = 0
        print("\n" + "="*60)
        print("Starting Login Level 2 Test Execution")
        print("="*60)

    def setUp(self):
        # ---------------------------
        # Disable ALL Chrome popups
        # ---------------------------
        options = webdriver.ChromeOptions()

        # Disable automation infobar
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Disable save-password popup + password leak popup
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,

            # Disable Chrome password leak detection
            "profile.password_manager_leak_detection": False,
            "profile.exit_type": "Normal",

            # Disable translate popup
            "translate.enabled": False,

            # Disable notification permission popups
            "profile.default_content_setting_values.notifications": 2,

            # Disable autofill
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,

            # Disable popup blocking message
            "profile.default_content_setting_values.popups": 0,

            # Disable Chrome startup restore popup
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
        options.add_experimental_option("prefs", prefs)

        # Reduce logging
        options.add_argument("--log-level=3")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins-discovery")

        # Start Chrome
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(TEST_CONFIG['implicit_wait'])
        self.driver.set_page_load_timeout(TEST_CONFIG['page_load_timeout'])
        self.wait = WebDriverWait(self.driver, TEST_CONFIG['explicit_wait'])
        self.current_test_id = None


    def tearDown(self):
        self.driver.quit()

    def find_element_by_config(self, key):
        locator_type, locator_value = LOCATORS[key]
        by_type = getattr(By, locator_type.upper())
        return self.driver.find_element(by_type, locator_value)

    def wait_for_element(self, key, timeout=None):
        if timeout is None:
            timeout = TEST_CONFIG['explicit_wait']
        locator_type, locator_value = LOCATORS[key]
        by_type = getattr(By, locator_type.upper())
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by_type, locator_value))
        )

    def do_login(self, username, password):
        self.driver.get(BASE_URL)
        time.sleep(1)
        # username
        uname = self.wait_for_element('username_field')
        uname.clear()
        if username is not None:
            # CSV may include quoted whitespace — keep as-is; an empty string will be ''
            uname.send_keys(username)
        # password
        pwd = self.find_element_by_config('password_field')
        pwd.clear()
        if password is not None:
            pwd.send_keys(password)
        # click login
        self.find_element_by_config('login_button').click()
        time.sleep(1)

    def validate(self, expected):
        page = self.driver.page_source
        url = self.driver.current_url.lower()

        if expected == "success":
            # presence of inventory marker
            try:
                self.driver.find_element(*self._tuple_from_locator(LOCATORS['inventory_page_marker']))
                return True
            except NoSuchElementException:
                return False

        if expected == "username_required":
            return EXPECTED_VALUES['username_required'].lower() in page.lower()

        if expected == "password_required":
            return EXPECTED_VALUES['password_required'].lower() in page.lower()

        if expected == "locked_out":
            return EXPECTED_VALUES['locked_out'].lower() in page.lower()

        if expected == "invalid_credentials":
            return EXPECTED_VALUES['invalid_credentials'].lower() in page.lower()

        return False

    def _tuple_from_locator(self, loc):
        by_type = getattr(By, loc[0].upper())
        return (by_type, loc[1])

    @data(*load_test_data())
    def test_login(self, test_case):
        self.current_test_id = test_case['test_case_id']
        LoginLevel2.total_tests += 1
        print(f"\nExecuting: {test_case['test_case_id']} - {test_case.get('test_description','')}")
        try:
            self.do_login(test_case['username'], test_case['password'])
            result = self.validate(test_case['expected'])
            if result:
                print(f" Test Case {self.current_test_id} PASSED")
                LoginLevel2.test_results['passed'].append(self.current_test_id)
            else:
                raise AssertionError(f"Validation failed for expected: {test_case['expected']}")
        except AssertionError as e:
            print(f" Test Case {self.current_test_id} FAILED: {e}")
            LoginLevel2.test_results['failed'].append({'test_id': self.current_test_id, 'reason': str(e)})
            raise
        except Exception as e:
            print(f" Test Case {self.current_test_id} ERROR: {e}")
            LoginLevel2.test_results['errors'].append({'test_id': self.current_test_id, 'reason': str(e)})
            raise

    @classmethod
    def tearDownClass(cls):
        print("\n" + "="*60)
        print("TEST EXECUTION SUMMARY - LOGIN LEVEL 2")
        print("="*60)
        print(f"Total Tests: {cls.total_tests}")
        print(f"Passed: {len(cls.test_results['passed'])}")
        print(f"Failed: {len(cls.test_results['failed'])}")
        print(f"Errors: {len(cls.test_results['errors'])}")
        print("="*60)
        if cls.test_results['failed']:
            print("\nFAILED TEST CASES:")
            for f in cls.test_results['failed']:
                print(f" - {f['test_id']}: {f['reason']}")
        if cls.test_results['errors']:
            print("\nERROR TEST CASES:")
            for e in cls.test_results['errors']:
                print(f" - {e['test_id']}: {e['reason']}")
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    unittest.main(verbosity=2)
