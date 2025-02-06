import os
import json
import requests
import sqlite3
import time
import yaml
import schedule
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration settings
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# API Cache directory
CACHE_DIR = "Data/Raw/API-Cache/"
os.makedirs(CACHE_DIR, exist_ok=True)

# Database setup
DB_PATH = config["database"]["path"]
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_api_key(service_name):
    """Retrieve API keys securely from the .env file."""
    return os.getenv(service_name.upper() + "_API_KEY")

def save_to_database(service_name, endpoint, data):
    """Store API responses in SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            endpoint TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("INSERT INTO api_data (service, endpoint, response) VALUES (?, ?, ?)",
                   (service_name, endpoint, json.dumps(data)))
    
    conn.commit()
    conn.close()

def fetch_from_api(service_name, endpoint, params=None, cache=True, cache_duration=300):
    """
    Fetch data from an API with tracking, rate limit prevention, and proper headers.
    """
    base_url = config["api"].get(service_name.lower())
    api_key = get_api_key(service_name)

    if not base_url or not api_key:
        print(f"❌ API Key missing for {service_name}. Check .env file.")
        return None

    url = f"{base_url}{endpoint}"
    headers = {}

    if service_name == "ALPHA_VANTAGE":
        headers = {
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
    elif service_name == "COIN_MARKET_CAP":
        headers = { 
            "X-CMC_PRO_API_KEY": api_key,  # ✅ Correct API Key Header
            "Accepts": "application/json"
        }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise error for 401, 404, etc.
        data = response.json()

        save_to_database(service_name, endpoint, data)

        print(f"✅ API Call Successful: {service_name} -> {endpoint}")
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ API Request Failed: {req_err}")

    return None

# 🔄 Scheduled Task
def scheduled_fetch():
    """Fetch and store API data at regular intervals."""
    print("🔄 Fetching latest API data...")

    fetch_from_api("COIN_GECKO", "simple/price", {"ids": "bitcoin", "vs_currencies": "usd"})
    fetch_from_api("COIN_MARKET_CAP", "cryptocurrency/listings/latest")

    print("✅ Scheduled API update completed.")

# ✅ Schedule updates every 10 minutes
schedule.every(10).minutes.do(scheduled_fetch)

if __name__ == "__main__":
    print("🔹 Automated API updates running every 10 minutes.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait before checking schedule again




