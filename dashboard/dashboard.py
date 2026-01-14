import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.engine import engine  # Your centralized engine

# --- Streamlit page config ---
st.set_page_config(page_title="Payroll Risk Dashboard", layout="wide")
st.title("Payroll Risk Dashboard")

# --- Load data from MySQL ---
@st.cache_data(ttl=300)
def load_data():
    with engine.begin() as conn:
        # Pull payroll risk scores
        risk_df = pd.read_sql(text("SELECT * FROM payroll_risk_scores"), conn)
        # Pull payroll signals if needed
        signals_df = pd.read_sql(text("SELECT * FROM payroll_signals"), conn)
    return risk_df, signals_df

risk_df, signals_df = load_data()

# --- Filters ---
st.sidebar.header("Filters")
departments = signals_df["department"].unique().tolist()
pay_periods = pd.to_datetime(signals_df["pay_period"]).dt.strftime('%Y-%m').unique().tolist()
risk_levels = risk_df["risk_level"].unique().tolist()

selected_dept = st.sidebar.multiselect("Department", options=departments, default=departments)
selected_period = st.sidebar.multiselect("Pay Period (YYYY-MM)", options=pay_periods, default=pay_periods)
selected_risk = st.sidebar.multiselect("Risk Level", options=risk_levels, default=risk_levels)

# --- Merge risk info with signals for display ---
merged_df = pd.merge(signals_df, risk_df, on=["employee_id", "pay_period"])
merged_df["pay_period"] = pd.to_datetime(merged_df["pay_period"]).dt.strftime('%Y-%m')

# Apply filters
filtered_df = merged_df[
    (merged_df["department"].isin(selected_dept)) &
    (merged_df["pay_period"].isin(selected_period)) &
    (merged_df["risk_level"].isin(selected_risk))
]

# --- Highlight HIGH risk rows ---
def highlight_high_risk(row):
    return ['background-color: #ff9999' if row.risk_level == 'HIGH' else '' for _ in row]

st.subheader(f"Filtered Payroll Risk Data ({len(filtered_df)} rows)")
st.dataframe(filtered_df.style.apply(highlight_high_risk, axis=1))

# --- Summary metrics ---
st.subheader("Summary")
st.metric("Total Employees", filtered_df["employee_id"].nunique())
st.metric("HIGH Risk Employees", len(filtered_df[filtered_df["risk_level"] == "HIGH"]))
st.metric("MEDIUM Risk Employees", len(filtered_df[filtered_df["risk_level"] == "MEDIUM"]))
st.metric("LOW Risk Employees", len(filtered_df[filtered_df["risk_level"] == "LOW"]))

# Optional: show charts
st.subheader("Risk Distribution by Department")
dept_chart = filtered_df.groupby(["department", "risk_level"]).size().unstack(fill_value=0)
st.bar_chart(dept_chart)
