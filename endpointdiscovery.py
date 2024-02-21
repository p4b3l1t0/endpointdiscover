puedes ver el error en la linea>

import requests
from bs4 import BeautifulSoup
import re
import argparse
from termcolor import colored

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', required=True, help="The domain to analyze, e.g., 'https://example.com'")
parser.add_argument('-ne', '--no-errors', action='store_true', help="Skip printing 404 errors")
parser.add_argument('-we', '--without-ext', action='store_true', help="Skip endpoints ending with a file extension")
parser.add_argument('-o', '--output', help="Save the output to a file")
args = parser.parse_args()

# Prepare the domain for the request
domain = args.domain
if not domain.startswith('http'):
    domain = 'http://' + domain

# Function to extract all .js links from a domain
def extract_js_links(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        script_tags = soup.find_all('script', src=True)
        js_links = [tag['src'] if tag['src'].startswith('http') else url + tag['src'] for tag in script_tags]
        return js_links
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return []

# Function to search in common JS file directories
def search_js_folders(base_url):
    common_paths = ['static/js', 'assets/js', '_next/static/chunks']
    found_js_files = []
    for path in common_paths:
        full_path = f"{base_url}/{path}"
        js_links = extract_js_links(full_path)
        found_js_files.extend(js_links)
    return found_js_files

# Function to extract endpoints from JS files
def extract_endpoints(js_urls, without_ext=False):
    endpoints = []
    for js_url in js_urls:
        try:
            js_content = requests.get(js_url).text
            # Simplification: search for URLs inside the JS file
            potential_urls = re.findall(r'https?://[^\s"\']+|/[^/\s"\']+[^\s"\';]+', js_content)
            if without_ext:
                # Filter out URLs ending in a known file extension
                potential_urls = [url for url in potential_urls if not re.search(r'\.(js|html|woff2|pdf|txt|css|tsx|ts)$', url)]
            endpoints.extend(potential_urls)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {js_url}: {e}")
    return endpoints

# Function to make GET requests to endpoints and colorize the output
def verificar_endpoints(domain, endpoints, no_errors=False, output_file=None):
    with open(output_file, 'w') if output_file else None as f:
        for endpoint in endpoints:
            url = f"{domain}{endpoint}" if not endpoint.startswith('http') else endpoint
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    msg = colored(f"{response.status_code} OK - {url}", "green")
                elif response.status_code == 404 and no_errors:
                    continue  # Skip printing 404 if no_errors is True
                elif response.status_code in [403, 500] or response.status_code != 200:
                    msg = colored(f"{response.status_code} - {url}", "blue")
                if f:
                    f.write(f"{msg}\n")
                print(msg)
            except Exception as e:
                if not no_errors:  # Print errors only if no_errors is False
                    error_msg = colored(f"Error accessing {url}: {e}", "red")
                    if f:
                        f.write(f"{error_msg}\n")
                    print(error_msg)

# Main execution
js_links_initial = extract_js_links(domain)
js_links_folders = search_js_folders(domain)
all_js_links = list(set(js_links_initial + js_links_folders))
endpoints = extract_endpoints(all_js_links, args.without_ext)
verificar_endpoints(domain, endpoints, args.no_errors, args.output)


