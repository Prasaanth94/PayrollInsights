import pandas as pd
import os
import shutil


SOURCE_DIR = "data_generator/output"
RAW_DIR = "data/raw"

REQUIRED_COLUMNS = [
    "employee_id",
    "employee_name",
    "department",
    "role",
    "base_salary",
    "overtime_pay",
    "bonus",
    "deductions",
    "net_pay",
    "pay_period"
]

def extract_payroll(filename: str) -> pd.DataFrame:
    source_path = os.path.join(SOURCE_DIR, filename)
    raw_path = os.path.join(RAW_DIR, filename)

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File not found: {source_path}")
    
    df = pd.read_csv(source_path)

    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    os.makedirs(RAW_DIR, exist_ok=True)

    #copu file exactly into raw
    shutil.copy(source_path, raw_path)
    

    return df