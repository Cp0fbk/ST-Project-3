# Search Test Configuration

BASE_URL = "https://ecommerce-playground.lambdatest.io/"
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# Locators
SEARCH_INPUT = ("name", "search")
SEARCH_BUTTON = ("xpath", "//button[@type='submit']")
PRODUCT_CONTAINER = ("id", "product-search")
PRODUCT_TITLES = ("xpath", "//h4[@class='title']/a")
NO_PRODUCT_MSG = ("xpath", "//p[contains(text(),'no product')]")
RESULT_INFO = ("xpath", "//div[@id='entry_212470']//div[@class='col-sm-12 text-end']")

# Test Data
TEST_DATA_FILE = "search_test_data.csv"