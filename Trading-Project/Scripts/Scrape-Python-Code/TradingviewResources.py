from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening the browser window
driver = webdriver.Chrome(service=service, options=options)

# Open the Pine Script documentation
url = "https://www.tradingview.com/pine-script-reference/v6/"
driver.get(url)

# Wait for the content to load
wait = WebDriverWait(driver, 20)

try:
    # Locate the main content container
    main_content = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#tvcontent div.tv-script-refrence__right-colums"))
    )

    # Extract main topics (H2)
    h2_elements = main_content.find_elements(By.CSS_SELECTOR, "div.tv-script-refrence__content-container h2")

    extracted_data = []

    for h2 in h2_elements:
        main_topic = h2.text
        sub_topics = h2.find_elements(By.XPATH, "following-sibling::h3")

        for h3 in sub_topics:
            sub_topic = h3.text
            definition_elements = h3.find_elements(By.XPATH, "following-sibling::div[contains(@class, 'tv-pine-reference-item__txt tv-txt')]")

            for definition in definition_elements:
                definition_text = definition.text.strip()
                extracted_data.append({
                    "Main Topic": main_topic,
                    "Sub Topic": sub_topic,
                    "Definition": definition_text
                })
                print(f"Extracted: {main_topic} -> {sub_topic}")

    # Save extracted content to a file
    with open("pine_script_reference_data.txt", "w", encoding="utf-8") as file:
        for item in extracted_data:
            file.write(f"{item['Main Topic']}\n{item['Sub Topic']}\n{item['Definition']}\n\n")

    print("Content extraction complete. Saved to pine_script_reference_data.txt")

except Exception as e:
    print(f"Error extracting content: {e}")

# Close the browser
driver.quit()













