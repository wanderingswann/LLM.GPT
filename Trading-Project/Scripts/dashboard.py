import sqlite3
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DB_PATH = "Data/database.db"

def fetch_api_data():
    """Retrieve API data from the database and return as a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT response, timestamp FROM api_data WHERE service='COIN_GECKO' AND endpoint='simple/price'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    prices = []
    timestamps = []

    for row in rows:
        response_data = json.loads(row[0])
        if "bitcoin" in response_data:
            prices.append(response_data["bitcoin"]["usd"])
            timestamps.append(row[1])

    df = pd.DataFrame({"Timestamp": timestamps, "Bitcoin Price (USD)": prices})
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

def fetch_custom_data():
    """Retrieve custom stored data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT category, data, timestamp FROM custom_data"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["Category", "Data", "Timestamp"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

# Streamlit Dashboard
st.title("📊 Crypto Trading Dashboard")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Prices", "Custom Data Insights"])

if page == "Market Prices":
    st.subheader("📈 Bitcoin Price Trends")

    df = fetch_api_data()
    if df.empty:
        st.warning("No market data available.")
    else:
        st.line_chart(df.set_index("Timestamp"))

        # Show raw data
        st.subheader("📄 Raw Market Data")
        st.dataframe(df)

elif page == "Custom Data Insights":
    st.subheader("📝 Custom Trading Insights")

    df = fetch_custom_data()
    if df.empty:
        st.warning("No custom data available.")
    else:
        st.dataframe(df)

st.sidebar.info("Data is sourced from CoinGecko and manually entered insights.")
