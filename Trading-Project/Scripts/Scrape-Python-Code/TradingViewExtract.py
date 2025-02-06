import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Base URL of the documentation
base_url = "https://www.tradingview.com/pine-script-docs/welcome/"

# User-Agent rotation to avoid detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
]

# Function to setup Selenium
def setup_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to get all section links from the aside navigation
def get_section_links(url):
    driver = setup_selenium()
    driver.get(url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Find the sidebar navigation inside the div#page-container > aside
    aside = soup.select_one("div#page-container aside#nav ul.toc")
    
    section_links = []
    if aside:
        for link in aside.find_all('a', href=True):
            href = link['href']
            full_url = f"https://www.tradingview.com{href}" if href.startswith('/pine-script-docs/') else href
            if full_url not in section_links:
                section_links.append(full_url)

    print(f"Found {len(section_links)} section links.")
    return section_links

# Function to scrape content from the main section of the page
def scrape_page_content(url):
    driver = setup_selenium()
    driver.get(url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extract the main content inside div#page-container > main
    main_content = soup.select_one("div#page-container main.main-pane")

    if not main_content:
        return None

    # Extract headings and paragraphs separately
    data = []
    current_heading = "No Title"

    for element in main_content.find_all(['h1', 'h2', 'h3', 'p', 'pre']):
        if element.name in ['h1', 'h2', 'h3']:
            current_heading = element.get_text(strip=True)
        elif element.name == 'p':
            paragraph = element.get_text(strip=True)
            data.append({"Title": current_heading, "Content": paragraph, "URL": url})
        elif element.name == 'pre':
            code_snippet = element.get_text(strip=True)
            data.append({"Title": current_heading, "Content": f"Code:\n{code_snippet}", "URL": url})

    return data

# Main function to scrape all sections
def scrape_all_sections():
    section_links = get_section_links(base_url)
    all_data = []

    for idx, link in enumerate(section_links):
        print(f"Scraping {idx + 1}/{len(section_links)}: {link}")
        retries = 3
        for attempt in range(retries):
            try:
                page_data = scrape_page_content(link)
                if page_data:
                    all_data.extend(page_data)
                time.sleep(random.uniform(2, 5))  # Random delay to avoid detection
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {link}: {e}")
                time.sleep(5)

    # Save to CSV
    if all_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        df = pd.DataFrame(all_data)
        filename = f"pine_script_docs_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"Scraped data saved to {filename}")
    else:
        print("No data scraped.")

# Run the scraper
scrape_all_sections()



