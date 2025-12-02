# -*- coding: utf-8 -*-
"""
Test Runner - Execute all data-driven tests
"""
import unittest
import sys
import os
from datetime import datetime


def run_level1_tests():
    """Run Level 1 data-driven tests"""
    print("\n" + "="*70)
    print("RUNNING LEVEL 1: DATA-DRIVEN TESTING")
    print("="*70)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName('test_level1_data_driven.DataDrivenPriceFilterTest')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def run_level2_tests():
    """Run Level 2 advanced data-driven tests"""
    print("\n" + "="*70)
    print("RUNNING LEVEL 2: ADVANCED DATA-DRIVEN TESTING WITH CONFIG")
    print("="*70)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName('test_level2_data_driven.AdvancedDataDrivenTest')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def main():
    """Main test runner"""
    print("\n" + "="*70)
    print(f"TEST EXECUTION STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Run Level 1 tests
    result1 = run_level1_tests()
    
    # Run Level 2 tests
    result2 = run_level2_tests()
    
    # Print final summary
    print("\n" + "="*70)
    print("FINAL TEST SUMMARY")
    print("="*70)
    print(f"Level 1 - Tests Run: {result1.testsRun}, Failures: {len(result1.failures)}, Errors: {len(result1.errors)}")
    print(f"Level 2 - Tests Run: {result2.testsRun}, Failures: {len(result2.failures)}, Errors: {len(result2.errors)}")
    print(f"\nTotal Tests: {result1.testsRun + result2.testsRun}")
    print(f"Total Failures: {len(result1.failures) + len(result2.failures)}")
    print(f"Total Errors: {len(result1.errors) + len(result2.errors)}")
    print("="*70)
    print(f"TEST EXECUTION COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()