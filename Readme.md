# ST-Project-3: Data-Driven Web UI Testing (Selenium + unittest + CSV)

This project contains data-driven Selenium tests in two levels:
- Level 1: simple tests with locators and logic inside the test files
- Level 2: advanced tests with configuration files (URLs, locators, timeouts) and CSV test data

Targets:
- https://ecommerce-playground.lambdatest.io/ (search, price filter, cart, view product, change password)
- https://www.saucedemo.com/ (login, logout)

## Requirements

- Python 3.8+
- Google Chrome installed
- ChromeDriver installed and available in PATH
  - Some files use a hardcoded driver path. Update these if needed:
    - level-1/Add to cart/add_to_cart_level1.py (Service(r"D:\drivers\chromedriver.exe"))
    - level-1/Remove from cart/remove_from_cart_level1.py (Service(r"D:\drivers\chromedriver.exe"))
    - level-2/Add to cart/add_to_cart_level2.py (Service(r"D:\drivers\chromedriver.exe"))
    - level-2/Remove from cart/remove_from_cart_level2.py (Service(r"D:\drivers\chromedriver.exe"))

Install libraries:
```bash
pip install selenium ddt
```

Optional (virtual environment):
```bash
python -m venv .venv
.venv\Scripts\activate
pip install selenium ddt
```

## Project Structure (high level)

- level-1/
  - Add to cart, Remove from cart, Search, PriceFilter, Login, Logout, View_product_detail
  - Each feature has a Python test file and CSV test data in the same folder
- level-2/
  - Same features, but with config files (py/json) + CSVs
- CSV test data are always colocated with their test file
- Some Level 2 features use config modules, e.g.:
  - level-2/Search/search_config.py
  - level-2/PriceFilter/price_filter_config.py
  - level-2/Login/login_config.py
  - level-2/Logout/logout_config.py

## How to Run

Important: run all commands from inside the ST-Project-3 directory.

General discovery:
```bash
# All Level 1 tests that use unittest
python -m unittest discover -s "level-1" -p "*_level1.py" -v

# All Level 2 tests that use unittest
python -m unittest discover -s "level-2" -p "*_level2.py" -v
```

Run a single module (unittest-based):
```bash
# Level 1
python -m unittest level-1.PriceFilter.price_filter_level1 -v
python -m unittest level-1.Search.search_level1 -v
python -m unittest level-1."Add to cart".add_to_cart_level1 -v
python -m unittest level-1."Remove from cart".remove_from_cart_level1 -v

# Level 2
python -m unittest level-2.PriceFilter.price_filter_level2 -v
python -m unittest level-2.Search.search_level2 -v
python -m unittest level-2.Login.login_level2 -v
python -m unittest level-2.Logout.logout_level2 -v
python -m unittest level-2."Add to cart".add_to_cart_level2 -v
python -m unittest level-2."Remove from cart".remove_from_cart_level2 -v
```

Run a specific test class or method (examples):
```bash
python -m unittest level-1.PriceFilter.price_filter_level1.PriceFilterLevel1 -v
python -m unittest level-2.PriceFilter.price_filter_level2.PriceFilterLevel2 -v
```

Run direct script-style tests (no unittest runner):
```bash
# Level 1 scripts
python "level-1\Login\login_level1.py"
python "level-1\Logout\logout_level1.py"
python "level-1\Change password\change_password_level1.py"
python "level-1\View_product_detail\view_product_detail_level1.py"

# Level 2 scripts
python "level-2\View_product_detail\view_product_detail_level2.py"
```

Notes:
- For Level 2 modules that import config from the same folder, sys.path is adjusted in code. Just run from project root as shown.
- If Windows blocks Chrome popups or password manager, most tests already disable them via ChromeOptions.

## Test Data and Configuration

- CSVs live next to their tests and are auto-loaded:
  - Level 1: search_test_data1.csv, search_test_data2.csv, price_filter_test_data.csv, add_to_cart_test_data.csv, remove_from_cart_test_data.csv, view_product_detail_test_data.csv, change_password_test_data.csv
  - Level 2: similar CSVs plus config files (json/py) for URLs, locators, wait times, and expected values
- Examples:
  - Price Filter L1: level-1/PriceFilter/price_filter_test_data.csv
  - Price Filter L2: level-2/PriceFilter/price_filter_test_data.csv + price_filter_config.py
  - Search L2: level-2/Search/search_test_data1.csv, search_test_data2.csv + search_config.py
  - Login/Logout L2: login_config.py / logout_config.py

## Troubleshooting

- ChromeDriver not found: put chromedriver.exe on PATH or update the Service(...) path in files listed above.
- Import errors: ensure you run from ST-Project-3. For Level 2, configs are in the same folder and sys.path is set in code.
- Slow page loads: increase explicit/implicit waits in the corresponding config (Level 2) or inside the test file (Level 1).

## Examples

- Level 1 classes: PriceFilter tests ([price_filter_level1.py](level-1/PriceFilter/price_filter_level1.py)), Search tests ([search_level1.py](level-1/Search/search_level1.py))
- Level 2 classes: PriceFilter tests ([price_filter_level2.py](level-2/PriceFilter/price_filter_level2.py)), Search tests ([search_level2.py](level-2/Search/search_level2.py)), Login ([login_level2.py](level-2/Login/login_level2.py)), Logout ([logout_level2.py](level-2/Logout/logout_level2.py))
