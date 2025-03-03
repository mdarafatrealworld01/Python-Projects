#pip install streamlit yfinance pandas plotly ta

#building real-time stock price dashboard

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

# Set the title of the dashboard
st.title("📈 Real-time Stock Price Dashboard")

# Sidebar for user input
st.sidebar.header("User Input")

# Stock ticker input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL").upper()

# Time period selection
time_period = st.sidebar.selectbox("Select Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])

# Fetch stock data
try:
    data = yf.download(ticker, period=time_period, interval='5m')
    if data.empty:
        st.error("No data found. Please enter a valid stock ticker.")
    else:
        # Display real-time stock price
        st.subheader(f"Real-time Price for {ticker}")
        st.write(f"Latest Close Price: **${data['Close'].iloc[-1]:.2f}**")

        # Plotting the stock data
        fig = go.Figure()

        # Candlestick chart
        fig.add_trace(go.Candlestick(x=data.index,
                                      open=data['Open'],
                                      high=data['High'],
                                      low=data['Low'],
                                      close=data['Close'],
                                      name='Candlestick'))

        # Adding technical indicators
        data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
        data['EMA20'] = ta.trend.ema_indicator(data['Close'], window=20)

        # Plotting SMA and EMA
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], mode='lines', name='SMA 20', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], mode='lines', name='EMA 20', line=dict(color='orange')))

        # Update layout
        fig.update_layout(title=f"{ticker} Stock Price", xaxis_title="Date", yaxis_title="Price (USD)", template="plotly_dark")

        # Show the plot
        st.plotly_chart(fig)

        # Display historical data
        st.subheader("📊 Historical Data")
        st.write(data.tail(20))  # Show last 20 records
except Exception as e:
    st.error(f"An error occurred: {e}")


#running this program use this command: streamlit run stock_dashboard.py