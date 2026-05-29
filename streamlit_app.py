import streamlit as st
import pandas as pd

st.set_page_config(page_title="FY26 Accounts Dashboard", layout="wide")
st.title("📊 FY26 Accounts Dashboard")

# 1. Sidebar Uploaders
st.sidebar.header("Upload Data Files")
expenses_file = st.sidebar.file_uploader("Upload Expenses CSV", type=["csv"])
invoices_file = st.sidebar.file_uploader("Upload Invoices CSV", type=["csv"])

# 2. Processing Logic
if expenses_file and invoices_file:
    # Load and clean Expenses
    df_exp = pd.read_csv(expenses_file)
    df_exp['Type'] = 'Expense'
    
    # Load and clean Invoices
    df_inv = pd.read_csv(invoices_file)
    df_inv['Type'] = 'Invoice'
    
    # Merge them into one big list
    df = pd.concat([df_exp, df_inv], ignore_index=True)
    
    # Clean the 'Gross' column (Remove $ , and handle parenthesis for negatives)
    def clean_gross(val):
        if isinstance(val, str):
            val = val.replace('$', '').replace(',', '')
            if '(' in val: # Handle (100.00) as -100.00
                val = '-' + val.replace('(', '').replace(')', '')
            return float(val)
        return val

    df['Gross'] = df['Gross'].apply(clean_gross)
    
    st.success("Files merged successfully!")

    # 3. Simple Dashboard Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Expenses", f"${df[df['Type']=='Expense']['Gross'].sum():,.2f}")
    col2.metric("Total Invoiced", f"${df[df['Type']=='Invoice']['Gross'].sum():,.2f}")

    # 4. View Data
    st.subheader("Data Overview")
    st.dataframe(df)
    
else:
    st.info("👈 Please upload **both** your Expenses CSV and your Invoices CSV in the sidebar to begin.")

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
