import csv
import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://www.pinecoders.com/techniques/dsp/"  # Replace with the actual URL

# Fetch page content
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Function to clean and return text safely
def clean_text(element):
    return " ".join(element.get_text(strip=True, separator=" ").split())

# Elements to capture in the correct order
elements_to_capture = ["h1", "h2", "h3", "h4", "p", "ul", "blockquote", "div"]

# Extract data while preserving order
data = []

for element in soup.find_all(elements_to_capture):
    tag_name = element.name

    # Handle blockquote paragraphs
    if tag_name == "blockquote":
        for p in element.find_all("p"):
            data.append(("blockquote > p", clean_text(p)))

    # Handle unordered lists <ul>
    elif tag_name == "ul":
        items = [clean_text(li) for li in element.find_all("li")]
        data.append(("ul", "; ".join(items)))

    # Handle code snippets within nested divs
    elif tag_name == "div" and "language-plaintext highlighter-rogue" in element.get("class", []):
        highlight_div = element.find("div", class_="highlight")
        if highlight_div:
            pre = highlight_div.find("pre", class_="highlight")
            if pre:
                code = pre.find("code")
                if code:
                    data.append(("code", clean_text(code)))

    # Handle headers and paragraphs normally
    else:
        data.append((tag_name, clean_text(element)))

# Save the extracted data to a CSV file
csv_file = "scraped_data_ordered.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Tag", "Content"])  # CSV header
    for tag, content in data:
        writer.writerow([tag, content])

print(f"Data successfully saved to {csv_file}")

# Debugging output to verify the captured order
for tag, content in data:
    print(f"{tag.upper()}:\n{content}\n{'-'*50}")



