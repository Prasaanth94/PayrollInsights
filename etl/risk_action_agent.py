import pandas as pd
from sqlalchemy import text
from db.engine import engine
from etl.alerts import send_alert

def run_risk_agent():
    print("Running Payroll risk agent...")

    # Read payroll signals into a DataFrame
    df = pd.read_sql("""
        SELECT
            employee_id,
            pay_period,
            net_pay_mismatch,
            high_overtime_flag,
            low_net_pay_flag,
            department_deviation_pct,
            salary_spike_flag
        FROM payroll_signals
    """, engine)

    # Initialize risk score and reasons
    df["risk_score"] = 0
    df["reasons"] = ""

    for idx, row in df.iterrows():
        reasons = []

        if row["net_pay_mismatch"] == 1:
            row["risk_score"] += 40
            reasons.append("Net pay mismatch")

        if row["salary_spike_flag"] == 1:
            row["risk_score"] += 40
            reasons.append("Salary spike")

        if row["high_overtime_flag"] == 1:
            row["risk_score"] += 25
            reasons.append("High overtime")

        if row["low_net_pay_flag"] == 1:
            row["risk_score"] += 30
            reasons.append("Low net pay vs department")

        if abs(row["department_deviation_pct"] or 0) > 30:
            row["risk_score"] += 30
            reasons.append("High deviation from department avg")

        # Update DataFrame
        df.at[idx, "risk_score"] = row["risk_score"]
        df.at[idx, "reasons"] = ", ".join(reasons)

    # Determine risk level
    def classify(score):
        if score >= 30:
            return "HIGH"
        elif score >= 20:
            return "MEDIUM"
        else:
            return "LOW"

    df["risk_level"] = df["risk_score"].apply(classify)

    # Save to payroll_risk_scores table
    df[["employee_id", "pay_period", "risk_score", "risk_level", "reasons"]].to_sql(
        "payroll_risk_scores",
        engine,
        if_exists="replace",  # or "append" if you want to preserve previous cycles
        index=False
    )

   
