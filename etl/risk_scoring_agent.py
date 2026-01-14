import pandas as pd
from sqlalchemy import text
from db.engine import engine

import os

def run_payroll_agent():
    print("Rynning payroll agent...")

    with engine.begin() as conn:
        query = ("""
            SELECT
                s.employee_id,
                s.pay_period,
                s.net_pay_mismatch,
                s.overtime_ratio,
                s.high_overtime_flag,
                s.department_deviation_pct,
                s.salary_spike_flag,
                s.low_net_pay_flag
            FROM payroll_signals s    

        """)

        df = pd.read_sql(query, engine)
        #agent reasoning
        df["risk_score"] = 0

        df.loc[df["net_pay_mismatch"] == 1, "risk_score"] +=3
        df.loc[df["high_overtime_flag"] == 1, "risk_score"] +=2
        df.loc[df["salary_spike_flag"] == 1, "risk_score"] +=2
        df.loc[df["low_net_pay_flag"] == 1, "risk_score"] +=2
        df.loc[df["overtime_ratio"] > 0.30, "risk_score"] +=2
        df.loc[df["department_deviation_pct"].abs() > 30, "risk_score"] +=1


        #risk levels
        def classify(score):
            if score >= 5:
                return "HIGH"
            elif score >= 3:
                return "MEDIUM"
            return "LOW"
        

        df["risk_level"] = df["risk_score"].apply(classify)

        #agent decision
        def decide_action(level):
            if level == "HIGH":
                return "Immediate HR Review"
            elif level == "MEDIUM":
                return "Manager Review"
            return "No action"
        
        df["recommended_action"] = df["risk_level"].apply(decide_action)

        df[[
            "employee_id",
            "pay_period",
            "risk_score",
            "risk_level",
            "recommended_action"
        ]].to_sql(
            "payroll_risk_actions",
            engine,
            if_exists="replace",
            index=False
        )

        print("Payroll risk agent completed")
          