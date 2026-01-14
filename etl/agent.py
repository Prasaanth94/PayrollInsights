import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = "payroll_app"
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "payroll"

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

def run_payroll_agen():
    print("Rynning payroll agent...")

    query = """
        SELECT
            s.eomployeed_id,
            s.pay_period,
            s.net_pay_mismatch,
            s.overtime_ratio.
            s.high_overtime_flag,
            s.department_deviation_pct,
            s.salary_spike_flag,
            s.low_net_pay_flag
        FROM payroll_signals s    

    """

    df = pd.read_sql(query, engine)

    df["risk_score"] = 0

    df.loc[df["net_pay_mismatch"] == 1, "risk_score"] +=3