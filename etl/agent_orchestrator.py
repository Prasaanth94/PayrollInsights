# etl/agent_orchestrator.py
import pandas as pd
from sqlalchemy import text
from db.engine import engine

class PayrollAgent:
    """
    Agentic AI orchestrator for payroll risk management.
    """

    def __init__(self):
        self.signals_table = "payroll_signals"
        self.actions_table = "payroll_risk_actions"
        print("PayrollAgent initialized.")

    def fetch_signals(self) -> pd.DataFrame:
        """
        Pull the latest payroll signals from the database.
        """
        print("Fetching payroll signals from DB...")
        query = f"""
            SELECT *
            FROM {self.signals_table};
        """
        df = pd.read_sql(query, engine)
        print(f"Fetched {len(df)} rows of signals.")
        return df

    def compute_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Multi-step reasoning to calculate risk scores and levels.
        """
        print("Computing risk scores...")
        df["risk_score"] = 0

        # Basic rules
        df.loc[df["net_pay_mismatch"] == 1, "risk_score"] += 3
        df.loc[df["high_overtime_flag"] == 1, "risk_score"] += 2
        df.loc[df["salary_spike_flag"] == 1, "risk_score"] += 2
        df.loc[df["low_net_pay_flag"] == 1, "risk_score"] += 2
        df.loc[df["overtime_ratio"] > 0.30, "risk_score"] += 2
        df.loc[df["department_deviation_pct"].abs() > 30, "risk_score"] += 1

        # Optional: more advanced reasoning could go here
        # e.g., ML model predictions or historical anomaly detection

        # Classify risk levels
        def classify(score):
            if score >= 5:
                return "HIGH"
            elif score >= 3:
                return "MEDIUM"
            return "LOW"

        df["risk_level"] = df["risk_score"].apply(classify)

        # Decide recommended action
        def decide_action(level):
            if level == "HIGH":
                return "Immediate HR Review"
            elif level == "MEDIUM":
                return "Manager Review"
            return "No action"

        df["recommended_action"] = df["risk_level"].apply(decide_action)
        print("Risk scores computed.")
        return df

    def save_actions(self, df: pd.DataFrame):
        """
        Save the agent decisions to the database.
        """
        print(f"Saving decisions to {self.actions_table}...")
        df[[
            "employee_id",
            "pay_period",
            "risk_score",
            "risk_level",
            "recommended_action"
        ]].to_sql(
            self.actions_table,
            engine,
            if_exists="replace",  # overwrite previous month
            index=False
        )
        print("Decisions saved successfully.")

    def run(self):
        """
        Full orchestration of the payroll agent.
        """
        print("Running Payroll Agent Orchestrator...")
        df_signals = self.fetch_signals()
        df_risk = self.compute_risk_scores(df_signals)
        self.save_actions(df_risk)
        print("Payroll Agent run completed.")


# Entry point
if __name__ == "__main__":
    agent = PayrollAgent()
    agent.run()
