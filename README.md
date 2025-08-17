# IB Flex Query Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A clean, modern Python client for downloading Interactive Brokers flex statements with custom date range support.

## Features

- 📅 **Custom date ranges** - Download statements for specific periods
- 🖥️ **CLI & API** - Use from command line or import as module  
- 🔒 **Secure** - Comprehensive `.gitignore` protects credentials
- ⚡ **Fast** - Efficient API calls with proper error handling
- 📁 **Auto-organize** - Creates directories automatically

## Quick Start

### 1. Setup
```bash
# Clone and install
git clone <repo-url>
cd ib-flex-query
uv sync

# Configure credentials
cp .env.example .env
# Edit .env with your IB token and query ID
```

### 2. Usage

**Command Line:**
```bash
# Default range
uv run python app.py

# Custom date range
uv run python app.py -s 2024-01-01 -e 2024-12-31 -o statements/2024.csv
```

**Python API:**
```python
from app import get_flex_statement

# Get statement with date range
file_path = get_flex_statement(
    start_date="2024-01-01",
    end_date="2024-12-31",
    output_path="data/my_statement.csv"
)
```

## CLI Options

| Option | Short | Description | Example |
|--------|--------|-------------|---------|
| `--start-date` | `-s` | Start date (YYYY-MM-DD) | `2024-01-01` |
| `--end-date` | `-e` | End date (YYYY-MM-DD) | `2024-12-31` |
| `--output` | `-o` | Output file path | `statements/jan.csv` |
| `--help` | `-h` | Show help | |

⚠️ **Important**: Date parameters may be ignored if your IB Flex Query template has a fixed date range. Check your flex query configuration in IB Account Management.

## API Reference

```python
def get_flex_statement(output_path=None, start_date=None, end_date=None):
    """
    Download IB flex statement.
    
    Args:
        output_path: Where to save (default: data/processed/flex_statement.csv)
        start_date: Start date as string "YYYY-MM-DD" or date object
        end_date: End date as string "YYYY-MM-DD" or date object
    
    Returns:
        Path: Location of downloaded file
        
    Note:
        Date parameters may be ignored if the IB Flex Query template 
        has a fixed date range configured.
    """
```

## Configuration

Create `.env` file with your IB credentials:

```bash
TOKEN="your_flex_query_token"
QUERY_ID="your_query_id"
```

**Getting IB credentials:**
1. Login to IB Account Management
2. Go to Reports → Flex Queries
3. Create query → Generate token
4. Note the Query ID and Token

## Examples

See `example_usage.py` for detailed usage patterns:

```python
# Various date formats supported
get_flex_statement(start_date="2024-01-01")           # String
get_flex_statement(start_date=date(2024, 1, 1))      # Date object
get_flex_statement(start_date="2024-06-01")          # Only start date
```

## Security

- 🔒 Credentials protected by comprehensive `.gitignore`
- 🛡️ See `SECURITY.md` for detailed security guidelines
- 🔑 `.env` file permissions automatically secured (600)

## License

MIT License - see [LICENSE](LICENSE) file for details.
