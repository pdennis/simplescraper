import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Set up Chrome in headless mode"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def get_links(url):
    """Fetch webpage and extract all links."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href and not href.startswith(('javascript:', '#', 'mailto:')):
                if not href.startswith(('http://', 'https://')):
                    if href.startswith('/'):
                        href = '/'.join(url.split('/')[:3]) + href
                    else:
                        href = url.rstrip('/') + '/' + href
                links.append(href)
        
        print("\nFound links:")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")
            
        return links
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

def parse_selection(selection, max_index):
    """Parse user selection string into list of indices."""
    indices = set()
    parts = selection.replace(' ', '').split(',')
    
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                indices.update(range(start, end + 1))
            except ValueError:
                print(f"Invalid range: {part}")
        else:
            try:
                indices.add(int(part))
            except ValueError:
                print(f"Invalid number: {part}")
    
    valid_indices = {i for i in indices if 1 <= i <= max_index}
    return sorted(list(valid_indices))

def download_pages(links, selected_indices):
    """Download content from selected links and save to file."""
    driver = setup_driver()
    
    with open('downloaded_content.txt', 'w', encoding='utf-8') as f:
        for index in selected_indices:
            url = links[index - 1]
            print(f"\nDownloading: {url}")
            
            try:
                driver.get(url)
                # Wait for content to load
                time.sleep(5)  # Give JavaScript time to run
                
                # Write page header
                f.write(f"\n{'='*50}\n{url}\n{'='*50}\n\n")
                
                # Get the main content
                try:
                    # Wait for content to be present
                    main_content = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "main, article, .content, .post-content"))
                    )
                    content = main_content.text
                except:
                    # If no specific content container found, get all body text
                    content = driver.find_element(By.TAG_NAME, "body").text
                
                f.write(content + '\n\n')
                
            except Exception as e:
                f.write(f"Error downloading {url}: {e}\n\n")
                print(f"Error downloading {url}: {e}")
            
            # Be nice to the server
            time.sleep(2)
    
    driver.quit()
    print("\nAll content has been saved to 'downloaded_content.txt'")

def main():
    url = input("Enter the webpage URL: ")
    links = get_links(url)
    
    if links:
        print("\nEnter the numbers of links to download (e.g., '1-6, 12, 15, 22-36')")
        selection = input("Selection: ")
        
        selected_indices = parse_selection(selection, len(links))
        if selected_indices:
            print(f"\nWill download {len(selected_indices)} pages...")
            download_pages(links, selected_indices)
        else:
            print("No valid indices selected.")

if __name__ == "__main__":
    main()