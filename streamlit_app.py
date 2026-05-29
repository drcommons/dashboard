import streamlit as st
import pandas as pd

st.title("📊 FY26 Accounts Dashboard")

# Create a file uploader widget
uploaded_file = st.sidebar.file_uploader("Upload your FY26 Accounts CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Convert 'Gross' column as before...
    df['Gross'] = df['Gross'].replace(r'[\$,]', '', regex=True).astype(float)
    
    # Now continue with your charts/KPIs...
    st.success("Data loaded successfully!")
else:
    st.info("Please upload your CSV file in the sidebar to begin.")
    st.stop() # Stops the app until file is uploaded

# 1. Page Config
st.set_page_config(page_title="FY26 Accounts Dashboard", layout="wide")
st.title("📊 Business Performance Dashboard")

# 2. Load Data (Assumes your file is named accounts.csv)
@st.cache_data
def load_data():
    df = pd.read_csv('accounts.csv')
    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
    # Convert 'Gross' to numeric, removing commas
    df['Gross'] = df['Gross'].replace(r'[\$,]', '', regex=True).astype(float)
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Data")
account_filter = st.sidebar.multiselect("Select Account", options=df['Account'].unique())
event_filter = st.sidebar.multiselect("Select Event", options=df['Event'].dropna().unique())

if account_filter:
    df = df[df['Account'].isin(account_filter)]
if event_filter:
    df = df[df['Event'].isin(event_filter)]

# 4. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"${df['Gross'].sum():,.2f}")
col2.metric("Total Transactions", len(df))
col3.metric("Avg Expense", f"${df['Gross'].mean():,.2f}")

# 5. Visualizations
st.subheader("Spending by Category")
fig = px.bar(df, x='Account', y='Gross', color='Account', title="Total Spend by Category")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Table")
st.dataframe(df)
