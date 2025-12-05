# -*- coding: utf-8 -*-
import unittest
import csv
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    NoAlertPresentException,
    TimeoutException,
)


class AddToCartTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service = Service(r"D:\drivers\chromedriver.exe")   # chỉnh nếu khác
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)

        with open("add_to_cart_config.json", encoding="utf-8") as f:
            cls.config = json.load(f)

        cls.base_url = cls.config["url"]
        cls.accept_next_alert = True

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def get_element(self, key):
        element = self.__class__.config["elements"][key]
        by_map = {
            "xpath": By.XPATH,
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT,
        }
        return by_map[element["by"]], element["value"]

    def apply_filter(self, filter_key):
        driver = self.__class__.driver
        wait = WebDriverWait(driver, 10)

        by_tile, loc_tile = self.get_element("product_tile")
        tiles = driver.find_elements(by_tile, loc_tile)
        first_tile = tiles[0] if tiles else None

        try:
            driver.find_element(*self.get_element(filter_key)).click()
            if first_tile is not None:
                try:
                    wait.until(EC.staleness_of(first_tile))
                except TimeoutException:
                    pass
        except NoSuchElementException:
            pass

    def run_add_to_cart_test(self, tc_id, product, quantity,
                             size_option, stock_status, expected_message):
        driver = self.__class__.driver
        wait = WebDriverWait(driver, 10)

        driver.get(self.__class__.base_url)

        if stock_status == "IN_STOCK":
            driver.find_element(*self.get_element("shop_by_category_link")).click()
            driver.find_element(*self.get_element("desktops_menu_item")).click()
            self.apply_filter("filter_in_stock")
        else:
            if product in ("Palm Treo Pro", "iMac"):
                driver.find_element(*self.get_element("pc_img")).click()
            else:
                driver.find_element(*self.get_element("desktops_img")).click()
            self.apply_filter("filter_out_of_stock")

        try:
            prod_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, product))
            )
            prod_link.click()
        except TimeoutException:
            try:
                driver.find_element(By.XPATH, f"//img[@alt='{product}']").click()
            except Exception as e:
                self.fail(f"{tc_id}: Cannot open product '{product}' - {e}")
                return

        if stock_status == "IN_STOCK":
            if size_option == "Small":
                try:
                    size_select_elem = driver.find_element(*self.get_element("size_dropdown"))
                    Select(size_select_elem).select_by_visible_text("Small (+$12.00)")
                except NoSuchElementException:
                    self.fail(f"{tc_id}: Size dropdown not found for product requiring size")

            try:
                qty_input = driver.find_element(*self.get_element("quantity_input"))
                qty_input.clear()
                if quantity != "":
                    qty_input.send_keys(str(quantity))
            except NoSuchElementException:
                self.fail(f"{tc_id}: Quantity input not found")
                actual_msg = ""
            else:
                try:
                    driver.find_element(*self.get_element("add_to_cart_button")).click()
                except NoSuchElementException as e:
                    self.fail(f"{tc_id}: Add to Cart button not found - {e}")
                    actual_msg = ""
                else:
                    time.sleep(2)     

                    try:
                        actual_msg = driver.find_element(
                            *self.get_element("notification_message")
                        ).text.strip()
                    except NoSuchElementException:
                        actual_msg = ""

                    if not actual_msg:
                        try:
                            actual_msg = driver.find_element(
                                *self.get_element("size_error_message")
                            ).text.strip()
                        except NoSuchElementException:
                            actual_msg = ""
        else:
            try:
                qty_input = driver.find_element(*self.get_element("quantity_input"))
                qty_input.clear()
                if quantity != "":
                    qty_input.send_keys(str(quantity))
            except NoSuchElementException:
                pass

            try:
                actual_msg = driver.find_element(
                    *self.get_element("add_to_cart_button")
                ).text.strip()
            except NoSuchElementException:
                actual_msg = ""

        actual_msg_normalized = " ".join(actual_msg.split())
        expected_message_normalized = " ".join(expected_message.split())

        self.assertEqual(
            expected_message_normalized,
            actual_msg_normalized,
            msg=f"{tc_id}: EXPECT '{expected_message}' BUT GOT '{actual_msg_normalized}'"
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
    with open("add_to_cart_test_data.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            def test_func(self, row=row):
                self.run_add_to_cart_test(
                    row["tc_id"],
                    row["product"],
                    row["quantity"],
                    row["size_option"],
                    row["stock_status"],
                    row["expected_message"]
                )

            test_name = (
                f"test_{row['tc_id']}_{row['product']}"
                .replace(" ", "_")
                .replace('"', "")
            )
            setattr(AddToCartTest, test_name, test_func)


add_tests_from_csv()

if __name__ == "__main__":
    unittest.main()
