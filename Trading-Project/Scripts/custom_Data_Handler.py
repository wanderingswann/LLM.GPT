import sqlite3
import json
from datetime import datetime

DB_PATH = "Data/database.db"

def add_custom_data(category, data):
    """Insert manually collected data into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO custom_data (category, data) VALUES (?, ?)", 
                   (category, json.dumps(data)))
    
    conn.commit()
    conn.close()
    print(f"✅ Custom data added under category '{category}'.")

def get_custom_data(category=None):
    """Retrieve manually stored data from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT * FROM custom_data WHERE category=?", (category,))
    else:
        cursor.execute("SELECT * FROM custom_data")

    rows = cursor.fetchall()
    conn.close()

    print(f"📌 Retrieved {len(rows)} records.")
    for row in rows:
        print(row)

def delete_custom_data(category):
    """Delete manually stored data from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM custom_data WHERE category=?", (category,))
    
    conn.commit()
    conn.close()
    print(f"❌ Custom data under category '{category}' deleted.")

# Example Usage
if __name__ == "__main__":
    # Example: Add a custom trading insight
    add_custom_data("Market Sentiment", {"BTC": "Bullish", "ETH": "Neutral"})

    # Fetch all custom data
    get_custom_data()

    # Delete a category (uncomment to use)
    # delete_custom_data("Market Sentiment")
