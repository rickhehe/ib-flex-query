#!/usr/bin/env python3
"""
Example usage of the IB Flex Query system with custom date ranges
"""
from app import get_flex_statement
from datetime import date, datetime

def main():
    print("=== IB Flex Query Examples ===\n")
    
    # Example 1: Default - no date range specified
    print("1. Default download (no date range):")
    try:
        file_path = get_flex_statement()
        print(f"   ✓ Downloaded to: {file_path}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Example 2: Using string dates
    print("2. Custom date range with strings:")
    try:
        file_path = get_flex_statement(
            output_path="data/processed/january_2024.csv",
            start_date="2024-01-01",
            end_date="2024-01-31"
        )
        print(f"   ✓ Downloaded to: {file_path}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Example 3: Using date objects
    print("3. Custom date range with date objects:")
    try:
        file_path = get_flex_statement(
            output_path="data/processed/last_month.csv",
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 31)
        )
        print(f"   ✓ Downloaded to: {file_path}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Example 4: Only start date (up to current date)
    print("4. Only start date specified:")
    try:
        file_path = get_flex_statement(
            output_path="data/processed/from_june.csv",
            start_date="2024-06-01"
        )
        print(f"   ✓ Downloaded to: {file_path}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")

if __name__ == "__main__":
    main()
