# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-14

### Added
- Initial release of IB Flex Query Client
- Support for custom date ranges (start_date, end_date parameters)
- Command line interface with argparse
- Programmatic API for integration
- Comprehensive security with .gitignore
- MIT License
- Automatic directory creation
- Error handling and validation
- Support for multiple date formats (strings, date objects)
- Environment variable configuration
- Examples and documentation

### Features
- Download Interactive Brokers flex statements
- Custom date range support via API parameters
- CLI with short and long options (-s, --start-date, etc.)
- Secure credential handling via .env files
- Path handling with pathlib
- Request retry and timeout handling

### Security
- Comprehensive .gitignore for credentials and data
- .env.example template
- Security documentation (SECURITY.md)
- Proper file permissions (600 for .env)
- No sensitive data in version control
