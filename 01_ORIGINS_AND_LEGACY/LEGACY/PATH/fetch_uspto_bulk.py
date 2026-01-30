import requests
from bs4 import BeautifulSoup
import os
import argparse
from urllib.parse import urljoin

USPTO_BULK_URL = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/"

def list_years():
    """List available years from the primary directory."""
    try:
        r = requests.get(USPTO_BULK_URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        years = []
        for link in soup.find_all("a"):
            href = link.get("href")
            # Filter for year directories (format YYYY/)
            if href and href.strip("/").isdigit() and len(href.strip("/")) == 4:
                years.append(href.strip("/"))
        
        return sorted(years, reverse=True)
    except Exception as e:
        print(f"[!] Error listing years: {e}")
        return []

def list_files_in_year(year):
    """List zip files for a specific year."""
    year_url = urljoin(USPTO_BULK_URL, f"{year}/")
    try:
        r = requests.get(year_url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        files = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and (href.endswith(".zip") or href.endswith(".xml")):
                files.append(urljoin(year_url, href))
        
        return files
    except Exception as e:
        print(f"[!] Error accessing year {year}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="USPTO Bulk Data Fetcher")
    parser.add_argument("--list-years", action="store_true", help="List available years")
    parser.add_argument("--year", type=str, help="Target year to inspect (e.g., 2002)")
    parser.add_argument("--download", type=str, help="Specific file URL to download")
    
    args = parser.parse_args()
    
    print(f"[*] Connecting to {USPTO_BULK_URL}...")
    
    if args.list_years:
        years = list_years()
        print(f"[*] Available Years: {years}")
        return

    if args.year:
        print(f"[*] Listing files for {args.year}...")
        files = list_files_in_year(args.year)
        for f in files[:10]: # Show first 10
            print(f" - {f}")
        if len(files) > 10:
            print(f"... and {len(files)-10} more.")
        return

    # Default Inspection
    years = list_years()
    if years:
        print(f"[*] Latest Year: {years[0]}")
        print(f"[*] Oldest Year: {years[-1]}")
        
    print("\nUsage:")
    print("  python fetch_uspto_bulk.py --list-years")
    print("  python fetch_uspto_bulk.py --year 2002")

if __name__ == "__main__":
    main()
