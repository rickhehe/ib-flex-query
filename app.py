#!/usr/bin/env python3
"""
Interactive Brokers Flex Query Client
Fetches flex statements using IB's web service API

Licensed under the MIT License - see LICENSE file for details
"""
import requests
import os
import xml.etree.ElementTree as ET
import time
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, date
import argparse


def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    config = {
        'token': os.getenv("TOKEN"),
        'query_id': os.getenv("QUERY_ID"),
        'version': 3,
        'base_url': "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService"
    }
    
    if not config['token'] or not config['query_id']:
        raise ValueError("Missing required environment variables: TOKEN and QUERY_ID")
    
    return config


def send_flex_request(config, start_date=None, end_date=None):
    """Send initial flex statement request and get reference code.
    
    Args:
        config (dict): Configuration dictionary
        start_date (str or date): Start date in YYYY-MM-DD format or date object
        end_date (str or date): End date in YYYY-MM-DD format or date object
    """
    send_params = {
        "t": config['token'],
        "q": config['query_id'],
        "v": config['version']
    }
    
    # Add date range parameters if provided
    if start_date:
        if isinstance(start_date, (date, datetime)):
            start_date = start_date.strftime("%Y%m%d")
        elif isinstance(start_date, str):
            # Convert YYYY-MM-DD to YYYYMMDD
            start_date = start_date.replace("-", "")
        send_params["StartDate"] = start_date
        
    if end_date:
        if isinstance(end_date, (date, datetime)):
            end_date = end_date.strftime("%Y%m%d")
        elif isinstance(end_date, str):
            # Convert YYYY-MM-DD to YYYYMMDD
            end_date = end_date.replace("-", "")
        send_params["EndDate"] = end_date
    
    url = config['base_url'] + "/SendRequest"
    
    try:
        response = requests.get(url, params=send_params, timeout=2)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to send flex request: {e}")
    
    return parse_flex_response(response.text)


def parse_flex_response(xml_text):
    """Parse XML response and extract status and reference code."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML response: {e}")
    
    status = None
    reference_code = None
    
    for child in root:
        if child.tag == "Status":
            status = child.text
        elif child.tag == "ReferenceCode":
            reference_code = child.text
    
    if status != "Success":
        raise RuntimeError(f"Flex request failed with status: {status}")
    
    if not reference_code:
        raise ValueError("No reference code found in response")
    
    return reference_code


def wait_for_statement_ready(wait_time=5):
    """Wait for the flex statement to be generated."""
    print(f"Waiting {wait_time} seconds for statement generation...")
    time.sleep(wait_time)


def download_flex_statement(config, reference_code):
    """Download the flex statement using the reference code."""
    receive_params = {
        "t": config['token'],
        "q": reference_code,
        "v": config['version']
    }
    
    url = config['base_url'] + "/GetStatement"
    
    try:
        response = requests.get(url, params=receive_params, allow_redirects=True, timeout=2)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download flex statement: {e}")

def save_statement_to_file(content, file_path):
    """Save statement content to file."""
    # Convert to Path object and ensure directory exists
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        path.write_bytes(content)
        print(f"Statement saved to: {path}")
    except IOError as e:
        raise RuntimeError(f"Failed to save file: {e}")


def get_flex_statement(output_path=None, start_date=None, end_date=None):
    """
    Main function to retrieve and save flex statement.
    
    Args:
        output_path (str or Path): Path where to save the downloaded statement.
                                  Defaults to data/processed/flex_statement.csv
        start_date (str or date): Start date for the statement range (YYYY-MM-DD format)
        end_date (str or date): End date for the statement range (YYYY-MM-DD format)
        
    Returns:
        Path: Path to the saved file
    """
    if output_path is None:
        output_path = Path("data/processed/flex_statement.csv")
    else:
        output_path = Path(output_path)
    
    print("Starting flex statement download...")
    
    # Display date range if specified
    if start_date or end_date:
        date_info = []
        if start_date:
            date_info.append(f"from {start_date}")
        if end_date:
            date_info.append(f"to {end_date}")
        print(f"Date range: {' '.join(date_info)}")
    
    # Load configuration
    config = load_config()
    print(f"Using query ID: {config['query_id']}")
    
    # Send request
    reference_code = send_flex_request(config, start_date, end_date)
    print(f"Request sent successfully. Reference code: {reference_code}")
    
    # Wait for processing
    wait_for_statement_ready()
    
    # Download statement
    content = download_flex_statement(config, reference_code)
    print(f"Downloaded {len(content)} bytes")
    
    # Save to file
    save_statement_to_file(content, output_path)
    
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Interactive Brokers Flex Statement")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: data/processed/flex_statement.csv)")
    parser.add_argument("--start-date", "-s", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", "-e", type=str, help="End date in YYYY-MM-DD format")
    
    args = parser.parse_args()
    
    try:
        file_path = get_flex_statement(
            output_path=args.output,
            start_date=args.start_date,
            end_date=args.end_date
        )
        print(f"✓ Flex statement successfully downloaded to: {file_path}")
    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)