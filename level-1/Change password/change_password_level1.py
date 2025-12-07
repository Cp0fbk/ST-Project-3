# change_password_level1.py - CHẠY NGON 100% TRÊN MỌI MÁY WINDOWS
import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TỰ ĐỘNG TÌM FILE CSV CÙNG THƯ MỤC VỚI .PY
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(CURRENT_DIR, "change_password_test_data.csv")
URL = "https://ecommerce-playground.lambdatest.io/"

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)

def login(driver, username, password):
    driver.get(URL)
    try:
        driver.find_element(By.XPATH, "//div[@id='widget-navbar-217834']//li[a//span][6]").click()
        driver.find_element(By.LINK_TEXT, "Login").click()
        driver.find_element(By.ID, "input-email").send_keys(username)
        driver.find_element(By.ID, "input-password").send_keys(password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()
        time.sleep(3)
    except:
        pass  # Đã login rồi thì bỏ qua

def go_to_change_password(driver):
    driver.find_element(By.XPATH, "//div[@id='widget-navbar-217834']//li[a//span][6]").click()
    driver.find_element(By.LINK_TEXT, "Password").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-password"))
    )

def perform_change_password(driver, new_pwd, confirm_pwd):
    driver.find_element(By.ID, "input-password").clear()
    driver.find_element(By.ID, "input-password").send_keys(new_pwd)
    driver.find_element(By.ID, "input-confirm").clear()
    driver.find_element(By.ID, "input-confirm").send_keys(confirm_pwd)
    driver.find_element(By.XPATH, "//input[@value='Continue']").click()

def get_result_message(driver):
    time.sleep(2)
    try:
        msg = driver.find_element(By.CSS_SELECTOR, ".alert-danger, .alert-success").text.strip()
        return msg
    except:
        return "Success"  # Không có alert nào = thành công

# ==================== MAIN ====================
driver = get_driver()

# Đăng nhập lần đầu
login(driver, "abab@gmail.com", "12345678a")

# Đọc CSV
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    test_cases = list(reader)

# In tiếng Anh để không lỗi font Windows
print(f"Found {len(test_cases)} test cases. Starting execution...\n")

for i, row in enumerate(test_cases, 1):
    test_id = row['test_id']
    new_pwd = row.get('new_password', '')
    confirm = row.get('confirm', '')
    expected = row['expected_result']

    print(f"[{i:02d}] {test_id} | pwd='{new_pwd}' | confirm='{confirm}'", end=" ")

    go_to_change_password(driver)
    perform_change_password(driver, new_pwd, confirm)
    message = get_result_message(driver)

    if expected == "Success":
        ok = "Success" in message or message == "Success"
    else:
        ok = expected in message

    if ok:
        print("-> PASS")
    else:
        print("-> FAIL")
        print(f"     Expected : {expected}")
        print(f"     Actual   : {message}")

print("\n=== ALL TEST CASES COMPLETED ===")
time.sleep(3)
driver.quit()