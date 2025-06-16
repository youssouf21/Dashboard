import streamlit as st

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV files (adjust the file paths as needed)
fact_transactions = pd.read_csv(r'C:\Users\utente\Desktop\Morana HW 3\Fact_Transactions.csv')  # Changed file name
dim_time = pd.read_csv(r'C:\Users\utente\Desktop\Morana HW 3\Dim_Time.csv')
dim_symbol = pd.read_csv(r'C:\Users\utente\Desktop\Morana HW 3\Dim_Symbol.csv')
dim_transaction_type = pd.read_csv(r'C:\Users\utente\Desktop\Morana HW 3\Dim_TransactionType.csv')
dim_geography = pd.read_csv(r'C:\Users\utente\Desktop\Morana HW 3\Dim_Geography.csv')

# Merge fact table with dimension tables for enriched querying
merged = fact_transactions.merge(dim_transaction_type, on='TransactionTypeID', how='left') \
                          .merge(dim_time, on='TimeID', how='left') \
                          .merge(dim_symbol, on='SymbolID', how='left') \
                          .merge(dim_geography, on='GeographyID', how='left')

# Convert 'Date' column to datetime format
merged['Date'] = pd.to_datetime(merged['Date'], errors='coerce')

# Streamlit UI
st.title("📊 Time Analysis Dashboard")

# Sidebar for Date Range Filter
st.sidebar.header("Filter by Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"), key="start_date")
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"), key="end_date")

# Convert the start_date and end_date from datetime.date to pandas Timestamp (datetime format)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the merged data based on the selected date range
filtered_data = merged[(merged['Date'] >= start_date) & (merged['Date'] <= end_date)]

# Line chart for Total Number of Transactions (BUY + SELL) over Time
st.subheader(f"Total Number of Transactions in {start_date.month}/{start_date.year}")
transaction_count_by_date = filtered_data.groupby('Date').size().reset_index(name='Total_Transactions')
st.line_chart(transaction_count_by_date.set_index('Date'))

# Bar chart: Top 3 Traded Symbols by Transaction Count
st.subheader("Top 3 Traded Symbols by Transaction Count")
top_symbols = filtered_data['Symbol'].value_counts().nlargest(3)
st.bar_chart(top_symbols)

# Bar chart: Top 5 Sectors by Transaction Count
st.subheader("Top 5 Sectors by Transaction Count")
top_sectors = filtered_data['Sector'].value_counts().nlargest(5)
st.bar_chart(top_sectors)

# Bar chart: Top 5 Industries by Transaction Count
st.subheader("Top 5 Industries by Transaction Count")
top_industries = filtered_data['Industry'].value_counts().nlargest(5)
st.bar_chart(top_industries)
