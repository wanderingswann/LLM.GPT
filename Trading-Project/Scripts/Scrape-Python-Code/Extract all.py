import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Base URL of the documentation
base_url = "https://www.pinecoders.com/techniques/dsp/"

# User-Agent rotation to prevent detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
]

# Function to get all section links from the documentation
def get_section_links(base_url):
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links in the navigation or sidebar
    section_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/pine-script-docs/en/') and href not in section_links:
            full_url = f"https://www.tradingview.com{href}"
            section_links.append(full_url)
    
    return section_links

# Function to scrape content using Selenium (for dynamic content)
def scrape_page_with_selenium(url):
    print(f"Scraping with Selenium: {url}")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)  # Allow time for JavaScript to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    return soup

# Function to scrape content from a given page URL
def scrape_pine_script_page(url):
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException:
        soup = scrape_page_with_selenium(url)

    # Extract specific content sections based on class names
    content_sections = soup.find_all('div', class_='doc-content')

    data = []
    for section in content_sections:
        title_tag = section.find_previous('h1')
        title = title_tag.get_text(strip=True) if title_tag else 'Untitled'

        content = section.get_text(strip=True)
        
        # Check for preformatted code blocks
        code_tag = section.find_next('pre')
        code = code_tag.get_text(strip=True) if code_tag else ''

        data.append({
            "Title": title,
            "Content": content,
            "Code": code,
            "URL": url
        })

    return data

# Main function to scrape all section pages with retries
def scrape_all_sections():
    all_data = []
    section_links = get_section_links(base_url)
    
    print(f"Found {len(section_links)} section links to scrape.")

    for idx, link in enumerate(section_links):
        print(f"Scraping {idx+1}/{len(section_links)}: {link}")

        retries = 3
        for attempt in range(retries):
            try:
                page_data = scrape_pine_script_page(link)
                all_data.extend(page_data)
                time.sleep(random.uniform(2, 5))  # Random delay to avoid detection
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {link}: {e}")
                time.sleep(5)

    # Save to CSV or database
    if all_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        df = pd.DataFrame(all_data)
        filename = f"pine_script_docs_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"Scraped data saved to {filename}")
    else:
        print("No data was scraped.")

# Run the scraper
scrape_all_sections()

