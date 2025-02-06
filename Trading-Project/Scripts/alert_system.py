import sqlite3
import json
import time
import smtplib
from email.mime.text import MIMEText

DB_PATH = "Data/database.db"

# Define alert thresholds
ALERT_THRESHOLDS = {
    "bitcoin": {"low": 100000, "high": 110000},  # Adjust as needed
    "ethereum": {"low": 5000, "high": 6000},
}

def get_latest_price(crypto):
    """Retrieve the latest price of a cryptocurrency from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT response FROM api_data 
        WHERE service='COIN_GECKO' AND endpoint='simple/price' 
        ORDER BY timestamp DESC LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        data = json.loads(row[0])
        return data.get(crypto, {}).get("usd", None)
    return None

def send_email_alert(crypto, price, threshold_type):
    """Send an email alert when a price crosses a threshold."""
    sender_email = "your_email@gmail.com"
    recipient_email = "recipient_email@gmail.com"
    subject = f"🚨 {crypto.upper()} Price Alert: ${price}"
    body = f"The price of {crypto.upper()} has crossed the {threshold_type} threshold of ${ALERT_THRESHOLDS[crypto][threshold_type]}.\n\nCurrent Price: ${price}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        # Configure SMTP for Gmail (you may need to enable "Less Secure Apps" in Gmail settings)
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.login(sender_email, "your_app_password")  # Use an App Password for security
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.quit()
        print(f"📧 Email Alert Sent: {crypto.upper()} is ${price}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def check_price_alerts():
    """Check if prices cross alert thresholds."""
    for crypto, thresholds in ALERT_THRESHOLDS.items():
        price = get_latest_price(crypto)

        if price:
            if price <= thresholds["low"]:
                print(f"⚠️ {crypto.upper()} dropped below ${thresholds['low']}: Current Price ${price}")
                send_email_alert(crypto, price, "low")
            elif price >= thresholds["high"]:
                print(f"🚀 {crypto.upper()} surged above ${thresholds['high']}: Current Price ${price}")
                send_email_alert(crypto, price, "high")

if __name__ == "__main__":
    print("🔄 Monitoring price alerts every 5 minutes...")
    while True:
        check_price_alerts()
        time.sleep(300)  # Check every 5 minutes
