import pandas as pd
from sqlalchemy import text 
from db.engine import engine


class PayrollAgent:

    #agentic ai orchestrator for payrol risk management

    def __init__(self):
        self.signals_table = "payroll_signals"
        self.actions_table = "payroll_risk_actions"
        print("PayrollAgent initialized")

    def fetch_signals(self) -> pd.DataFrame:
        #fetching latest payroll signals
        print("Fetching payroll signals from DB...")
        query = f"""
            SELECT * 
            FROM {self.signals_table};
        """
        df = pd.read_sql(query, engine)
        print(f"Fetched {len(df)} rows of signals.")
        return df

    def compute_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
            #Multi step reasoning to calculate risk scores and levels