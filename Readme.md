# ST-Project-3: Data-Driven Testing Framework

This project contains data-driven tests for web application features organized into two levels of testing complexity.

## Project Structure

```
ST-Project-3/
├── level-1/
│   ├── PriceFilter/
│   │   ├── price_filter_level1.py        # Level 1 Price Filter tests
│   │   └── price_filter_test_data.csv    # Test data for Price Filter
│   └── Search/
│       └── test_data.csv                 # Test data for Search
├── level-2/
│   ├── PriceFilter/
│   │   ├── price_filter_config.py        # Configuration for Level 2 tests
│   │   ├── price_filter_level2.py        # Level 2 Price Filter tests
│   │   └── price_filter_test_data.csv    # Test data for Price Filter
│   └── Search/
│       └── test_data.csv                 # Test data for Search
├── .gitignore
└── Readme.md
```

## Prerequisites

- Python 3.x
- Selenium WebDriver
- ChromeDriver (or appropriate browser driver)
- DDT (Data-Driven Tests) library

Install required packages:
```bash
pip install selenium
pip install ddt
```

## Running Tests

**Important:** Run all commands from the `ST-Project-3` directory.

---

### Run Specific Test Cases

#### Run Level 1 Price Filter Tests Only

**Option 1: Using unittest module**
```bash
python -m unittest level-1.PriceFilter.price_filter_level1 -v
```

**Option 2: Run directly**
```bash
python level-1\PriceFilter\price_filter_level1.py
```

**Option 3: Navigate to directory and run**
```bash
cd level-1\PriceFilter
python price_filter_level1.py
cd ..\..
```

---

#### Run Level 2 Price Filter Tests Only

**Option 1: Using unittest module**
```bash
python -m unittest level-2.PriceFilter.price_filter_level2 -v
```

**Option 2: Run directly**
```bash
python level-2\PriceFilter\price_filter_level2.py
```

**Option 3: Navigate to directory and run**
```bash
cd level-2\PriceFilter
python price_filter_level2.py
cd ..\..
```

---

### Run Specific Test Methods or Test Classes

#### Run a specific test class

**Level 1:**
```bash
python -m unittest level-1.PriceFilter.price_filter_level1.DataDrivenPriceFilterTest -v
```

**Level 2:**
```bash
python -m unittest level-2.PriceFilter.price_filter_level2.AdvancedDataDrivenTest -v
```

#### Run a specific test method

**Level 1 - Single test case:**
```bash
python -m unittest level-1.PriceFilter.price_filter_level1.DataDrivenPriceFilterTest.test_price_filter_data_driven_1 -v
```

**Level 2 - Single test case:**
```bash
python -m unittest level-2.PriceFilter.price_filter_level2.AdvancedDataDrivenTest.test_advanced_price_filter_1 -v
```

---

## Test Data

Test data is stored in CSV files:

### Level 1: `price_filter_test_data.csv`
- Basic data-driven testing
- Contains test cases with price ranges and expected results
- Located in: `level-1/PriceFilter/`

### Level 2: `price_filter_test_data.csv`
- Advanced data-driven testing with configuration management
- Uses `price_filter_config.py` for centralized configuration
- Located in: `level-2/PriceFilter/`

You can modify the CSV files to add or change test cases.

---

## Configuration

### Level 1
- Uses hardcoded configuration within the test file
- Simple and straightforward approach

### Level 2
- Uses `price_filter_config.py` for centralized configuration
- Contains:
  - BASE_URL
  - LOCATORS (element identifiers)
  - TEST_CONFIG (timeouts, browser settings)
  - EXPECTED_VALUES

---

## Command Line Options

- `-v` or `--verbose`: Provides detailed test output
- `-k`: Run tests matching a pattern (Python 3.2+)
- `--failfast`: Stop on first failure
- `--buffer`: Buffer stdout/stderr during tests

**Example with options:**
```bash
python -m unittest discover -s level-1 -p "price_filter_level1.py" -v --failfast
```

---

## Troubleshooting

### Import Errors

If you encounter import errors, create `__init__.py` files:

```bash
type nul > level-1\__init__.py
type nul > level-1\PriceFilter\__init__.py
type nul > level-2\__init__.py
type nul > level-2\PriceFilter\__init__.py
```

### Config Import Issues (Level 2)

Make sure `price_filter_config.py` is in the same directory as `price_filter_level2.py`.

If still having issues, check that the sys.path is correctly configured in `price_filter_level2.py`:
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

---

## Test Execution Output

Successful test execution displays:
- Number of tests run
- Test results (OK/FAILED/ERROR)
- Execution time
- Detailed test case information (with -v flag)
- Individual data-driven test case results
- Browser automation in action (unless headless mode is enabled)

**Example output:**
```
test_price_filter_data_driven_1 (level-1.PriceFilter.price_filter_level1.DataDrivenPriceFilterTest) ... ok
test_price_filter_data_driven_2 (level-1.PriceFilter.price_filter_level1.DataDrivenPriceFilterTest) ... ok

----------------------------------------------------------------------
Ran 2 tests in 15.234s

OK
```
---

## File Naming Convention

- **Level 1 test files**: `price_filter_level1.py`
- **Level 2 test files**: `price_filter_level2.py`
- **Test data files**: `price_filter_test_data.csv`
- **Config files**: `price_filter_config.py` (Level 2 only)