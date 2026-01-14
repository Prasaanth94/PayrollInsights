import pandas as pd
from db.engine import engine




def load_to_mysql(file_path: str):
    """
    Load a CSV file into the 'payroll' table in MySQL.
    """
    print(f"Loading {file_path} into MySQL...")
    df = pd.read_csv(file_path)

    # Optional: clean column names (remove spaces, lowercase)
    df.columns = [col.strip() for col in df.columns]

    # Load into MySQL
    df.to_sql(
        name="payroll",
        con=engine,
        if_exists="append",  # append to existing table
        index=False
    )
    print(f"Successfully loaded {len(df)} rows into MySQL.")
