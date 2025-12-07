# view_product_detail_level1.py - LEVEL 1 - VIEW PRODUCT DETAIL - 100% ENGLISH OUTPUT
import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Auto find CSV in same folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(CURRENT_DIR, "view_product_detail_test_data.csv")
URL = "https://ecommerce-playground.lambdatest.io/"

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)

def is_product_page(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "h1")
        driver.find_element(By.CSS_SELECTOR, ".product-price, .price-new")
        return True
    except:
        return False

def is_not_found_page(driver):
    page_text = driver.page_source.lower()
    return any(keyword in page_text for keyword in ["not found", "404", "cannot be found", "product does not exist"])

def click_product_by_name(driver, product_name):
    try:
        img = driver.find_element(By.XPATH, f"//img[contains(@alt, '{product_name}')]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
        time.sleep(1)
        img.click()
        return True
    except:
        print(f"   [WARN] Product not found: {product_name}")
        return False

def click_category_image(driver, category_name):
    try:
        img = driver.find_element(By.XPATH, f"//img[@alt='{category_name}']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
        time.sleep(1)
        img.click()
        return True
    except:
        print(f"   [WARN] Category not found: {category_name}")
        return False

# ==================== MAIN ====================
driver = get_driver()
wait = WebDriverWait(driver, 15)

# Read CSV
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    tests = list(csv.DictReader(f))

print(f"Found {len(tests)} test cases. Starting execution...\n")

for i, row in enumerate(tests, 1):
    test_id = row['test_id']
    action = row['action']
    product_name = row.get('product_name', '').strip()
    product_id = row.get('product_id', '').strip()
    category = row.get('category', '').strip()
    expected = row['expected_result']

    print(f"[{i:02d}] {test_id:<12}", end=" ")

    driver.get(URL)
    time.sleep(3)

    success = False

    if action == "click_image" and product_name:
        if click_product_by_name(driver, product_name):
            time.sleep(3)
            success = is_product_page(driver)

    elif action == "click_category" and product_name and category:
        if click_category_image(driver, category):
            time.sleep(3)
            if click_product_by_name(driver, product_name):
                time.sleep(3)
                success = is_product_page(driver)

    elif action == "direct_url" and product_id:
        url = f"{URL}index.php?route=product/product&product_id={product_id}"
        driver.get(url)
        time.sleep(3)
        if "not found" in expected.lower():
            success = is_not_found_page(driver)
        else:
            success = is_product_page(driver)

    # Result
    if ("Product page displayed" in expected and success) or \
       ("not found" in expected.lower() and is_not_found_page(driver)):
        print("-> PASS")
    else:
        print("-> FAIL")
        print(f"     Expected : {expected}")
        print(f"     Current URL: {driver.current_url}")

print("\nALL TEST CASES COMPLETED SUCCESSFULLY!")
time.sleep(3)
driver.quit()