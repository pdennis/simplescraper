# Web Content Downloader

A Python script that allows you to download content from multiple web pages. The script displays all links on a given webpage, lets you select which ones to download, and saves their content to a single file.

## Features
- Lists all links found on an input webpage
- Supports selecting multiple pages using ranges (e.g., "1-5") and individual numbers (e.g., "1,3,7")
- Handles dynamically loaded JavaScript content
- Saves all downloaded content to a single file with clear separators
- Includes polite delays between requests

## Requirements
- Python 3.6+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install requests beautifulsoup4 selenium
   ```

## Usage
1. Run the script:
   ```bash
   python scraper.py
   ```

2. Enter the URL when prompted

3. Select which links to download using:
   - Ranges: "1-6"
   - Individual numbers: "8,12"
   - Combinations: "1-6,8,12,15-20"

4. The script will create `downloaded_content.txt` with the results

## Notes
- Respects server load with 2-second delays between requests
- Handles JavaScript-rendered content
- Works with relative and absolute URLs
