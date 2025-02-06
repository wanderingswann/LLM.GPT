import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_api_key(service_name):
    """
    Retrieve API keys from the .env file securely.
    Example: get_api_key("COIN_GECKO")
    """
    return os.getenv(service_name.upper() + "_API_KEY")

def load_config():
    """
    Load configuration settings from config.yaml.
    """
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

# Example usage
if __name__ == "__main__":
    config = load_config()
    coin_gecko_key = get_api_key("COIN_GECKO")

    print("✅ Config Loaded Successfully!")
    print("📌 API Base URL for CoinGecko:", config["api"]["coin_gecko"])
    print("🔑 CoinGecko API Key:", "Loaded" if coin_gecko_key else "Missing")
