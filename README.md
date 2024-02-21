# EndpointDiscover

`EndpointDiscover` is a Python-based tool developed to aid in the discovery of API endpoints hidden within JavaScript files of a web application. This tool is particularly useful for penetration testers and developers interested in uncovering endpoints that could potentially expose sensitive information or reveal functionalities not intended to be public.

## Features

- **JavaScript File Extraction**: Scans a given domain to identify and extract URLs of JavaScript files.
- **Endpoint Extraction**: Analyzes the JavaScript files to extract potential API endpoints.
- **HTTP Response Filtering**: Supports filtering endpoints based on their HTTP response codes to focus on potentially interesting or vulnerable endpoints.
- **File Extension Filtering**: Offers an option to exclude endpoints that end with specific file extensions, helping to narrow down the results to more relevant endpoints.
- **Customizable Options**: Includes flags for skipping 404 errors (`-ne` or `--no-errors` or ) and excluding endpoints with file extensions (`-we` or `--without-ext`), even if you want to save your endpoint list (`-o` or `--output`).

## Getting Started

### Prerequisites

- Python 3.x
- Requests library
- BeautifulSoup4 library
- termcolor library

You can install the necessary libraries using pip:

```bash
pip install requests beautifulsoup4 termcolor
```

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/p4b3l1t0/endpointdiscover.git
cd endpointdiscover
pip install -r requirements.txt
```
## Usage
To use the tool, run the following command from the terminal, replacing <domain> with the domain you wish to analyze:

Options:

* -d or --domain: Specify the domain to analyze (required).
* -ne or --no-errors: Skip printing 404 errors.
* -we or --without-ext: Skip endpoints ending with a file extension.
* -o or --output: Save results in a file.

## License

This project is licensed under the MIT License - see the https://chat.openai.com/c/LICENSE.md file for details.

