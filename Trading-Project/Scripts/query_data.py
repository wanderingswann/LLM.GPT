import sqlite3
import json
import pandas as pd

DB_PATH = "Data/database.db"

def get_api_data(service=None, endpoint=None, latest_only=False):
    """Retrieve API data from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM api_data WHERE 1=1"
    params = []

    if service:
        query += " AND service=?"
        params.append(service)
    if endpoint:
        query += " AND endpoint=?"
        params.append(endpoint)
    if latest_only:
        query += " ORDER BY timestamp DESC LIMIT 1"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    print(f"📌 Retrieved {len(rows)} records.")
    for row in rows:
        print(row)

def get_custom_data(category=None, latest_only=False):
    """Retrieve custom stored data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM custom_data WHERE 1=1"
    params = []

    if category:
        query += " AND category=?"
        params.append(category)
    if latest_only:
        query += " ORDER BY timestamp DESC LIMIT 1"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    print(f"📌 Retrieved {len(rows)} records.")
    for row in rows:
        print(row)

# Example Usage
if __name__ == "__main__":
    print("\n🔍 Fetching latest Bitcoin price from CoinGecko:")
    get_api_data(service="COIN_GECKO", endpoint="simple/price", latest_only=True)

    print("\n📊 Fetching all custom data:")
    get_custom_data()
