import pandas as pd
import numpy as np
import requests
import fitz  # PyMuPDF
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import streamlit as st

@st.cache_data
def extract_tax_data_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[4]  # Page 5 (index 4)
    text = page.get_text()
    pdf_document.close()
    
    pattern = re.compile(r'(\d{4}-\d{2})\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)')
    matches = pattern.findall(text)
    
    data = {"Year": [], "Total Taxes (Rs. crore)": []}
    for match in matches:
        year, direct_tax, indirect_tax, total_tax = match
        data["Year"].append(year)
        data["Total Taxes (Rs. crore)"].append(int(total_tax.replace(',', '')))
    
    return pd.DataFrame(data)

@st.cache_data
def calculate_forecast(df):
    df["Year"] = pd.to_datetime(df["Year"], format="%Y-%y")
    df.set_index("Year", inplace=True)
    
    # ARIMA Model
    arima_model = ARIMA(df['Total Taxes (Rs. crore)'], order=(2,1,2))
    arima_model_fit = arima_model.fit()
    future_arima = arima_model_fit.forecast(steps=5)
    
    # LSTM Model
    scaler = MinMaxScaler(feature_range=(0,1))
    data_scaled = scaler.fit_transform(df[['Total Taxes (Rs. crore)']])
    
    train_size = int(len(data_scaled) * 0.8)
    train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]
    
    def create_sequences(data, seq_length=3):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i+seq_length])
            y.append(data[i+seq_length])
        return np.array(X), np.array(y)
    
    X_train, y_train = create_sequences(train_data)
    X_test, y_test = create_sequences(test_data)
    
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)),
        LSTM(50, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=1, validation_data=(X_test, y_test))
    
    future_inputs = np.array([data_scaled[-3:]])
    future_lstm = scaler.inverse_transform(model.predict(future_inputs))
    
    return future_arima, future_lstm

def show_forecast():
    st.title("Tax Collection Forecast and Economic Analysis")

    st.markdown("""
    ### Understanding Taxes
    Taxes are mandatory financial charges imposed by the government on individuals and businesses. The revenue generated from taxes is used to fund various public services and infrastructure projects, such as healthcare, education, defense, and transportation. By collecting taxes, the government can provide essential services to its citizens and promote economic growth.

    ### Time Series Analysis
    Time series analysis involves analyzing data points collected or recorded at specific time intervals. In this app, we use time series analysis to forecast future tax collections based on historical data. This helps in understanding trends and making informed financial decisions.
    """)

    pdf_path = "time_series.pdf"
    df = extract_tax_data_from_pdf(pdf_path)
    
    if df.empty:
        st.error("No data extracted from the PDF.")
        return
    
    df["Year"] = pd.to_datetime(df["Year"], format="%Y-%y")
    df.set_index("Year", inplace=True)
    
    st.subheader("Historical Tax Liability Trends")
    st.markdown("This graph shows the historical tax collection data. Hover over the graph to see the value at each point.")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x=df.index, y='Total Taxes (Rs. crore)', marker='o', label='Total Tax Collection')
    plt.title("Historical Tax Liability Trends")
    plt.xlabel("Year")
    plt.ylabel("Tax Collected (Rs. crore)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    ### Explanation of Historical Trends
    The historical tax collection data shows the trends in tax revenue over the years. Various factors can influence these trends, including economic growth, changes in tax laws, and government policies. For example:
    - **Economic Growth**: During periods of economic growth, tax collections tend to increase as businesses and individuals earn more income.
    - **Tax Law Changes**: Changes in tax rates, exemptions, and deductions can impact the total tax collected.
    - **Government Policies**: Policies aimed at improving tax compliance and reducing tax evasion can lead to higher tax collections.
    """)

    st.subheader("Tax Collection Forecast (ARIMA Model)")
    st.markdown("The ARIMA model is used to forecast future tax collections based on historical data. This graph shows the forecasted tax collections for the next 5 years.")
    arima_model = ARIMA(df['Total Taxes (Rs. crore)'], order=(2,1,2))
    arima_model_fit = arima_model.fit()
    future_arima = arima_model_fit.forecast(steps=5)
    
    future_years = pd.date_range(start=df.index[-1], periods=6, freq='Y')[1:]
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Total Taxes (Rs. crore)'], label="Historical Data", marker='o')
    plt.plot(future_years, future_arima, label="ARIMA Forecast", linestyle='dashed', marker='o')
    plt.title("Tax Collection Forecast (ARIMA Model)")
    plt.xlabel("Year")
    plt.ylabel("Tax Collected (Rs. crore)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    ### Explanation of ARIMA Model Predictions
    The ARIMA model predictions provide an estimate of future tax collections based on past trends. This can help in understanding the expected revenue and planning for future expenditures. The forecasted values can be influenced by:
    - **Past Trends**: The model uses historical data to identify patterns and make predictions.
    - **Economic Conditions**: Future economic conditions can impact the accuracy of the predictions.
    """)

    st.subheader("Tax Collection Forecast (LSTM Model)")
    st.markdown("The LSTM model is a type of neural network used for time series forecasting. This graph shows the forecasted tax collections for the next year using the LSTM model.")
    scaler = MinMaxScaler(feature_range=(0,1))
    data_scaled = scaler.fit_transform(df[['Total Taxes (Rs. crore)']])
    
    train_size = int(len(data_scaled) * 0.8)
    train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]
    
    def create_sequences(data, seq_length=3):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i+seq_length])
            y.append(data[i+seq_length])
        return np.array(X), np.array(y)
    
    X_train, y_train = create_sequences(train_data)
    X_test, y_test = create_sequences(test_data)
    
    st.write("Please wait while the model is being trained...")
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)),
        LSTM(50, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=1, validation_data=(X_test, y_test))
    
    future_inputs = np.array([data_scaled[-3:]])
    future_lstm = scaler.inverse_transform(model.predict(future_inputs))
    
    st.write(f"LSTM Prediction for 2025: ₹{future_lstm[0][0]:,.2f} crore")
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Total Taxes (Rs. crore)'], label="Historical Data", marker='o')
    plt.axvline(df.index[-1], color='gray', linestyle='dashed', label="Prediction Start")
    plt.scatter(future_years[0], future_lstm[0][0], color='red', label="LSTM Forecast", marker='o')
    plt.title("Tax Collection Forecast (LSTM Model)")
    plt.xlabel("Year")
    plt.ylabel("Tax Collected (Rs. crore)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    st.markdown("""
    ### Explanation of LSTM Model Predictions
    The LSTM model predictions provide an estimate of future tax collections using a neural network approach. This can help in understanding the expected revenue and planning for future expenditures. The forecasted values can be influenced by:
    - **Past Trends**: The model uses historical data to identify patterns and make predictions.
    - **Economic Conditions**: Future economic conditions can impact the accuracy of the predictions.
    """)

# Call the function to display the forecast
# show_forecast()