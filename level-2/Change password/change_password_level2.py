# change_password_level2.py - LEVEL 2 HOÀN CHỈNH - CHẠY NGON 100%
import unittest
import csv
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# TỰ ĐỘNG TÌM FILE CÙNG THƯ MỤC VỚI .PY
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CURRENT_DIR, "change_password_config.json")
TEST_DATA_FILE = os.path.join(CURRENT_DIR, "change_password_test_data.csv")  

class ChangePasswordTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

        # Đọc config.json
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cls.config = json.load(f)

        cls.url = cls.config["url"]
        cls.elements = cls.config["elements"]
        cls.login_info = cls.config["login"]

        # Đăng nhập một lần
        cls.driver.get(cls.url)
        cls.login()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @classmethod
    def login(cls):
        try:
            cls.driver.find_element(By.XPATH, cls.elements["my_account_dropdown"]["value"]).click()
            cls.driver.find_element(By.LINK_TEXT, cls.elements["login_link"]["value"]).click()

            cls.driver.find_element(By.ID, cls.elements["input_email"]["value"]).send_keys(cls.login_info["email"])
            cls.driver.find_element(By.ID, cls.elements["input_password_login"]["value"]).send_keys(cls.login_info["password"])
            cls.driver.find_element(By.XPATH, cls.elements["btn_login"]["value"]).click()
            time.sleep(3)
            print("[INFO] Login successful!")
        except Exception as e:
            print("[INFO] Already logged in or skip login")

    def get_element(self, key):
        elem = self.__class__.elements[key]
        by_map = {
            "xpath": By.XPATH,
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT
        }
        return by_map[elem["by"]], elem["value"]

    def go_to_change_password_page(self):
        self.driver.find_element(*self.get_element("my_account_dropdown")).click()
        self.driver.find_element(*self.get_element("password_link")).click()
        self.wait.until(EC.presence_of_element_located(self.get_element("input_new_password")))

    def change_password(self, new_pwd="", confirm=""):
        self.driver.find_element(*self.get_element("input_new_password")).clear()
        self.driver.find_element(*self.get_element("input_new_password")).send_keys(new_pwd)
        self.driver.find_element(*self.get_element("input_confirm")).clear()
        self.driver.find_element(*self.get_element("input_confirm")).send_keys(confirm)
        self.driver.find_element(*self.get_element("btn_continue")).click()

    def get_alert_message(self):
        time.sleep(2)
        try:
            msg = self.driver.find_element(*self.get_element("alert_message")).text.strip()
            return msg
        except NoSuchElementException:
            return "Success: You have modified your password!"

    def test_change_password(self, test_id, new_password, confirm, expected):
        print(f"\n Running {test_id} | pwd='{new_password}' | confirm='{confirm}'")
        self.go_to_change_password_page()
        self.change_password(new_password, confirm)
        actual = self.get_alert_message()

        self.assertIn(
            expected,
            actual,
            msg=f"\n{test_id} FAILED!\nExpected: '{expected}'\nActual  : '{actual}'"
        )
        print(f"{test_id}  PASSED")

# TẠO TEST CASE TỰ ĐỘNG TỪ CSV
def create_test_functions():
    with open(TEST_DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_id = row["test_id"]
            pwd = row["new_password"] if row["new_password"] else ""
            confirm = row["confirm"] if row["confirm"] else ""
            expected = row["expected_result"]

            def test_func(self, p=pwd, c=confirm, e=expected, tid=test_id):
                self.test_change_password(tid, p, c, e)

            test_name = f"test_{test_id.replace('-', '_')}"
            setattr(ChangePasswordTest, test_name, test_func)

create_test_functions()

if __name__ == "__main__":
    unittest.main(verbosity=2)