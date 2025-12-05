# -*- coding: utf-8 -*-
import unittest
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    NoAlertPresentException,
    TimeoutException,
)

class RemoveFromCartTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # CHỈNH đường dẫn chromedriver cho đúng máy bạn
        service = Service(r"D:\drivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://ecommerce-playground.lambdatest.io/"
        cls.accept_next_alert = True

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def open_home(self):
        self.driver.get(self.base_url)

    def open_cart_page(self):
        self.driver.get(self.base_url + "index.php?route=checkout/cart")

    def clear_cart_completely(self):
        self.open_cart_page()
        while True:
            remove_buttons = self.driver.find_elements(
                By.XPATH,
                "//button[@data-original-title='Remove' or contains(@class,'btn-danger')]"
            )
            if not remove_buttons:
                break
            remove_buttons[0].click()
            time.sleep(1)

    def add_product(self, product_name, size_text=None, qty="1"):
        d = self.driver

        self.open_home()

        d.find_element(By.LINK_TEXT, "Shop by Category").click()
        d.find_element(
            By.XPATH,
            "//div[@id='widget-navbar-217841']/ul/li[7]/a/div[2]/span"
        ).click()

        first_tile = None
        try:
            tiles = d.find_elements(By.CSS_SELECTOR, "div.product-layout")
            if tiles:
                first_tile = tiles[0]
        except Exception:
            pass

        try:
            d.find_element(
                By.XPATH,
                "//div[@id='mz-filter-panel-0-5']//label[contains(.,'In stock')]"
            ).click()

            if first_tile is not None:
                try:
                    WebDriverWait(d, 10).until(EC.staleness_of(first_tile))
                except TimeoutException:
                    pass
        except NoSuchElementException:
            pass

        try:
            d.find_element(By.LINK_TEXT, product_name).click()
        except NoSuchElementException:
            d.find_element(By.XPATH, f"//img[@alt='{product_name}']").click()

        if size_text:
            try:
                from selenium.webdriver.support.ui import Select
                size_select = d.find_element(By.ID, "input-option234-216836")
                Select(size_select).select_by_visible_text(size_text)
            except NoSuchElementException:
                pass

        try:
            qty_input = d.find_element(By.XPATH, "//div[@id='entry_216841']//input")
            qty_input.clear()
            qty_input.send_keys(str(qty))
        except NoSuchElementException:
            pass

        d.find_element(By.XPATH, "//div[@id='entry_216842']//button").click()
        time.sleep(2)


    def prepare_cart_for_tc(self, tc_id, initial_items):
        self.clear_cart_completely()

        initial_items = int(initial_items)

        if initial_items == 0:
            pass
        elif initial_items == 1:
            self.add_product("iPod Touch", size_text=None, qty="1")
        elif initial_items >= 2:
            self.add_product("iPod Touch", size_text=None, qty="2")
            self.add_product("Samsung SyncMaster 941BW", size_text=None, qty="3")

        self.open_cart_page()

    def count_cart_rows(self):
        try:
            rows = self.driver.find_elements(
                By.XPATH, "//div[@id='content']//form//table/tbody/tr"
            )
            return len(rows)
        except NoSuchElementException:
            return 0

    def click_remove_once(self):
        d = self.driver
        remove_buttons = d.find_elements(
            By.XPATH,
            "//div[@id='content']/form/div/table/tbody/tr/td[4]/div/div/button[2]/i"
        )
        if remove_buttons:
            remove_buttons[0].click()
            time.sleep(1)

    def get_empty_cart_message(self):
        try:
            msg = self.driver.find_element(
                By.XPATH, "//div[@id='content']/p"
            ).text
            return msg.strip()
        except NoSuchElementException:
            return ""

    def has_continue_link(self):
        try:
            self.driver.find_element(By.LINK_TEXT, "Continue")
            return True
        except NoSuchElementException:
            return False

    def run_remove_cart_test(self, tc_id, initial_items,
                             remove_clicks, expected_items_after,
                             expect_empty_message):
        d = self.driver

        self.prepare_cart_for_tc(tc_id, initial_items)

        remove_clicks = int(remove_clicks)
        for _ in range(remove_clicks):
            self.click_remove_once()

        expected_items_after = int(expected_items_after)
        actual_items_after = self.count_cart_rows()
        self.assertEqual(
            expected_items_after,
            actual_items_after,
            msg=f"{tc_id}: EXPECT {expected_items_after} item(s) AFTER remove BUT GOT {actual_items_after}"
        )

        expect_empty = (expect_empty_message.strip().upper() == "YES")

        empty_msg = self.get_empty_cart_message()
        continue_exists = self.has_continue_link()

        if expect_empty:
            self.assertEqual(
                "Your shopping cart is empty!",
                empty_msg,
                msg=f"{tc_id}: EXPECT empty message BUT GOT '{empty_msg}'"
            )
            self.assertTrue(
                continue_exists,
                msg=f"{tc_id}: EXPECT 'Continue' link when cart empty"
            )
        else:
            self.assertNotEqual(
                "Your shopping cart is empty!",
                empty_msg,
                msg=f"{tc_id}: Cart should NOT be empty"
            )

    def is_alert_present(self):
        try:
            self.__class__.driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    def close_alert_and_get_its_text(self):
        try:
            alert = self.__class__.driver.switch_to.alert
            text = alert.text
            if self.__class__.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return text
        finally:
            self.__class__.accept_next_alert = True

def add_tests_from_csv():
    with open("remove_from_cart_test_data.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            def test_func(self, row=row):
                self.run_remove_cart_test(
                    row["tc_id"],
                    row["initial_items"],
                    row["remove_clicks"],
                    row["expected_items_after"],
                    row["expect_empty_message"],
                )

            test_name = f"test_{row['tc_id']}"
            setattr(RemoveFromCartTest, test_name, test_func)


add_tests_from_csv()

if __name__ == "__main__":
    unittest.main()