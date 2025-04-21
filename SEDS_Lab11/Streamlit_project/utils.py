import time
import pandas as pd
import streamlit as st


@st.cache_data
def fetch_bitcoin_data(start_date, end_date):
    try:
        start_timestamp = int(time.mktime(start_date.timetuple()))
        end_timestamp = int(time.mktime(end_date.timetuple()))

        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={start_timestamp}&to={end_timestamp}"

        # Fetch the data from the URL
        data = pd.read_json(url)

        # Check if data is empty
        if data.empty:
            print(f"No data fetched for the given range: {start_date} to {end_date}")
            return pd.DataFrame()

        # Process the data into DataFrames
        prices = pd.DataFrame(data['prices'].tolist(), columns=['Timestamp', 'Price'])
        market_caps = pd.DataFrame(data['market_caps'].tolist(), columns=['Timestamp', 'Market Cap'])
        total_volumes = pd.DataFrame(data['total_volumes'].tolist(), columns=['Timestamp', 'Total Volume'])

        # Combine the data into a single DataFrame
        df = prices.copy()
        df['Market Cap'] = market_caps['Market Cap']
        df['Total Volume'] = total_volumes['Total Volume']
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
        df = df[['Date', 'Price', 'Market Cap', 'Total Volume']]

        return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()
