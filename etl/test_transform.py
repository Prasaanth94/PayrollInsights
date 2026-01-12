from etl.extract import extract_payroll
from etl.transform import transform_payroll

if __name__ == "__main__":
    df_raw = extract_payroll("payroll_2026-01.csv")
    df_transformed = transform_payroll(df_raw)
    print(df_transformed.head())
