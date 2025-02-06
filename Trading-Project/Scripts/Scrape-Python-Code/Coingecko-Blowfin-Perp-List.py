import requests
import json

# Define the correct API URL
url = "https://api.coingecko.com/api/v3/derivatives/exchanges/blofin?include_tickers=all"

# Define headers
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "InsertYourAPIKeyHere"
}

try:
    # Make the request
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raise error for HTTP issues

    # Parse JSON response
    data = response.json()

    # Print the full response for debugging
    print("Full API Response:", json.dumps(data, indent=4))

    # Save to a JSON file
    with open("blofin_futures.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("✅ Data successfully saved to blofin_futures.json")

except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")















