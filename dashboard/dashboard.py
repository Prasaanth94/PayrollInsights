import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.engine import engine


# ------------------------------
# Streamlit page config
# ------------------------------
st.set_page_config(page_title="Payroll Risk Dashboard", layout="wide")
st.title("Payroll Risk Dashboard")


# ------------------------------
# Load data from MySQL
# ------------------------------
@st.cache_data(ttl=300)
def load_data():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT
                p.employee_id,
                p.employee_name,
                p.department,
                p.role,
                p.pay_period,
                r.risk_score,
                r.risk_level,
                r.reasons
            FROM payroll_risk_scores r
            JOIN payroll p
              ON r.employee_id = p.employee_id
             AND r.pay_period = p.pay_period
        """), conn)

    df["pay_period"] = pd.to_datetime(df["pay_period"]).dt.strftime("%Y-%m")
    return df


df = load_data()


# ------------------------------
# Sidebar Filters
# ------------------------------
st.sidebar.header("Filters")

departments = sorted(df["department"].unique())
pay_periods = sorted(df["pay_period"].unique())
risk_levels = ["LOW", "MEDIUM", "HIGH"]

selected_dept = st.sidebar.multiselect(
    "Department",
    options=departments,
    default=departments
)

selected_period = st.sidebar.multiselect(
    "Pay Period (YYYY-MM)",
    options=pay_periods,
    default=pay_periods
)

selected_risk = st.sidebar.multiselect(
    "Risk Level",
    options=risk_levels,
    default=risk_levels
)


# ------------------------------
# Apply filters
# ------------------------------
filtered_df = df[
    (df["department"].isin(selected_dept)) &
    (df["pay_period"].isin(selected_period)) &
    (df["risk_level"].isin(selected_risk))
]


# ------------------------------
# Highlight HIGH risk rows
# ------------------------------
def highlight_high_risk(row):
    if row.risk_level == "HIGH":
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)


st.subheader(f"Filtered Payroll Risk Data ({len(filtered_df)} rows)")
st.dataframe(filtered_df.style.apply(highlight_high_risk, axis=1), use_container_width=True)


# ------------------------------
# Summary Metrics
# ------------------------------
st.subheader("Risk Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Employees", filtered_df["employee_id"].nunique())
col2.metric("HIGH Risk", len(filtered_df[filtered_df["risk_level"] == "HIGH"]))
col3.metric("MEDIUM Risk", len(filtered_df[filtered_df["risk_level"] == "MEDIUM"]))
col4.metric("LOW Risk", len(filtered_df[filtered_df["risk_level"] == "LOW"]))


# ------------------------------
# Charts
# ------------------------------
st.subheader("Risk Distribution by Department")

dept_chart = (
    filtered_df
    .groupby(["department", "risk_level"])
    .size()
    .unstack(fill_value=0)
)

st.bar_chart(dept_chart)
