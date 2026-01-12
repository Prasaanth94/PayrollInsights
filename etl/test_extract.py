from etl.extract import extract_payroll

if __name__ == "__main__":
    # Provide path to one of your raw CSVs
    file_path = "data/raw/payroll_2026-01.csv"
    
    df = extract_payroll(file_path)
    print(df.head())  # Preview first 5 rows
