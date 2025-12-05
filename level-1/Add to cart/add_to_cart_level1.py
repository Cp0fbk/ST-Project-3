# -*- coding: utf-8 -*-
import unittest
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait 
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
        service = Service(r"D:\drivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://ecommerce-playground.lambdatest.io/"
        cls.accept_next_alert = True

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def run_add_to_cart_test(self, tc_id, product, quantity,
                             size_option, stock_status, expected_message):
        driver = self.__class__.driver
        driver.get(self.__class__.base_url)

        # 1. Vào category & filter theo stock 
        if stock_status == "IN_STOCK":
            driver.find_element(By.LINK_TEXT, "Shop by Category").click()
            driver.find_element(
                By.XPATH,
                "//div[@id='widget-navbar-217841']/ul/li[7]/a/div[2]/span"
            ).click()

            first_tile = None
            try:
                tiles = driver.find_elements(By.CSS_SELECTOR, "div.product-layout")
                if tiles:
                    first_tile = tiles[0]
            except Exception:
                pass

            try:
                driver.find_element(
                    By.XPATH,
                    "//div[@id='mz-filter-panel-0-5']//label[contains(.,'In stock')]"
                ).click()

                if first_tile is not None:
                    try:
                        WebDriverWait(driver, 10).until(EC.staleness_of(first_tile))
                    except TimeoutException:
                        pass
            except NoSuchElementException:
                pass

        else:  
            if product in ("Palm Treo Pro", "iMac"):
                driver.find_element(By.XPATH, "//img[@alt='PC']").click()
            else:
                driver.find_element(By.XPATH, "//img[@alt='Desktops']").click()

            first_tile = None
            try:
                tiles = driver.find_elements(By.CSS_SELECTOR, "div.product-layout")
                if tiles:
                    first_tile = tiles[0]
            except Exception:
                pass

            try:
                driver.find_element(
                    By.XPATH,
                    "//div[@id='mz-filter-panel-0-5']//div[2]//label"
                ).click()

                if first_tile is not None:
                    try:
                        WebDriverWait(driver, 10).until(EC.staleness_of(first_tile))
                    except TimeoutException:
                        pass
            except NoSuchElementException:
                pass

        try:
            driver.find_element(By.LINK_TEXT, product).click()
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, f"//img[@alt='{product}']").click()
            except Exception as e:
                self.fail(f"{tc_id}: Cannot open product '{product}' - {e}")
                return

        # 3. Xử lý theo stock status
        if stock_status == "IN_STOCK":
            # 3.1 Chọn size nếu cần
            if size_option == "Small":
                try:
                    Select(driver.find_element(By.ID, "input-option234-216836")) \
                        .select_by_visible_text("Small (+$12.00)")
                except NoSuchElementException:
                    self.fail(f"{tc_id}: Size dropdown not found for product requiring size")

            # 3.2 Nhập quantity
            try:
                qty_input = driver.find_element(By.XPATH, "//div[@id='entry_216841']//input")
                qty_input.clear()
                if quantity != "":
                    qty_input.send_keys(str(quantity))
            except NoSuchElementException:
                self.fail(f"{tc_id}: Quantity input not found")
                actual_msg = ""
            else:
                # 3.3 Click Add to cart
                try:
                    driver.find_element(By.XPATH, "//div[@id='entry_216842']//button").click()
                except NoSuchElementException as e:
                    self.fail(f"{tc_id}: Add to Cart button not found - {e}")
                    actual_msg = ""
                else:
                    # 3.4 Lấy notification message 
                    time.sleep(2)
                    try:
                        actual_msg = driver.find_element(
                            By.XPATH, "//div[@id='notification-box-top']//p"
                        ).text
                    except NoSuchElementException:
                        actual_msg = ""
                        
                    if not actual_msg:
                        try:
                            actual_msg = driver.find_element(
                                By.XPATH, "//div[@id='entry_216836']/form/div/div"
                            ).text
                        except NoSuchElementException:
                            actual_msg = ""
        else:
            try:
                qty_input = driver.find_element(By.XPATH, "//div[@id='entry_216841']//input")
                qty_input.clear()
                if quantity != "":
                    qty_input.send_keys(str(quantity))
            except NoSuchElementException:
                pass

            try:
                out_btn = driver.find_element(By.XPATH, "//div[@id='entry_216842']//button")
                actual_msg = out_btn.text
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
        for i, row in enumerate(reader):
            def test_func(self, row=row):
                self.run_add_to_cart_test(
                    row["tc_id"],
                    row["product"],
                    row["quantity"],
                    row["size_option"],
                    row["stock_status"],
                    row["expected_message"]
                )

            test_name = f"test_{row['tc_id']}_{row['product']}".replace(" ", "_").replace('"', '')
            setattr(AddToCartTest, test_name, test_func)


add_tests_from_csv()

if __name__ == "__main__":
    unittest.main()
