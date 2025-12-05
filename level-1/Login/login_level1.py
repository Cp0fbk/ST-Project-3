import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Load test data
def load_test_data(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def login_test(driver, username, password):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)

def validate_login(driver, expected):
    page = driver.page_source.lower()
    current_url = driver.current_url.lower()

    match expected:
        case "success": return "inventory" in current_url
        case "username_required": return "username is required" in page
        case "password_required": return "password is required" in page
        case "locked_out": return "locked out" in page
        case "invalid_credentials": return "do not match any user" in page
        case "invalid_or_truncate" | "secret_or_truncate": 
            return "inventory" not in current_url
        case _: return False

# ------------------- MAIN -------------------
chrome_options = Options()
chrome_options = Options()

# ---------- Disable general browser pop-ups ----------
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--disable-features=PasswordManagerUI,PasswordLeakDetection")
chrome_options.add_argument("--disable-features=AutofillServerCommunication")
chrome_options.add_argument("--disable-features=AutofillPruneSuggestions")

# ---------- Disable Chrome password manager ----------
prefs = {
    "credentials_enable_service": False,          # Disable Chrome Credential Service
    "profile.password_manager_enabled": False,    # Disable built-in password manager
    "profile.password_manager_leak_detection": False,  # Disable password leak popup
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.popups": 0,
    "autofill.profile_enabled": False,
    "autofill.credit_card_enabled": False,
    "autofill.password_manager_suppress_prompt": True,
}

chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)

data = load_test_data("login_test_data.csv")

for row in data:
    print(f"Running test: {row}")
    login_test(driver, row["username"], row["password"])
    result = validate_login(driver, row["expected"])
    print("Result:", "PASS" if result else "FAIL")

driver.quit()
