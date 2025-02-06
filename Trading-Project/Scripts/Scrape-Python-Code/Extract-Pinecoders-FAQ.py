import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Target documentation URL
url = "https://www.pinecoders.com/techniques/dsp/"

# Function to scrape content from TradingView Pine Script documentation
def scrape_pine_script_docs(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logging.info(f"Successfully accessed {url}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract headings and content
        data = []
        sections = soup.find_all(['h1', 'h2', 'h3'])

        for section in sections:
            title = section.get_text(strip=True)
            content_list = []
            code_list = []

            # Process siblings sequentially to maintain order
            next_element = section.find_next_sibling()
            while next_element and next_element.name not in ['h1', 'h2', 'h3']:
                # Extract paragraph content with inline code
                if next_element.name == 'p':
                    paragraph_text = []
                    for content in next_element.contents:
                        if content.name == 'code':
                            paragraph_text.append(f" `{content.get_text(strip=True)}` ")
                        elif isinstance(content, str):
                            paragraph_text.append(content.strip())

                    content_list.append(" ".join(paragraph_text))

                # Extract preformatted code blocks
                elif next_element.name == 'pre':
                    code_list.append(next_element.get_text(strip=True))

                # Handle <div class="highlight"> for code snippets
                elif next_element.name == 'div' and 'highlight' in next_element.get('class', []):
                    highlighted_code = next_element.find('code')
                    if highlighted_code:
                        code_list.append(highlighted_code.get_text(strip=True))

                # Find and include any other remaining inline code
                for code in next_element.find_all('code'):
                    code_list.append(code.get_text(strip=True))

                next_element = next_element.find_next_sibling() if next_element else None

            # Combine content and code properly while preserving order and formatting
            combined_content = " ".join(content_list).strip()
            combined_code = "\n".join(code_list).strip()

            data.append({
                "Title": title,
                "Content": combined_content,
                "Code": combined_code
            })

        # Save extracted data to CSV with a timestamp
        if data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pine_script_documentation_{timestamp}.csv"
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            logging.info(f"Scraped data saved to {filename}")
            return df
        else:
            logging.warning("No relevant data found on the page.")
            return None

    except requests.exceptions.Timeout:
        logging.error("Request timed out. The server took too long to respond.")
    except requests.exceptions.ConnectionError:
        logging.error("Failed to connect to the website. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except AttributeError as e:
        logging.error(f"Attribute error occurred: {e}. A tag may not exist.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Run the scraper
scraped_data = scrape_pine_script_docs(url)

if scraped_data is not None:
    print(scraped_data.head())
else:
    print("No data extracted.")






