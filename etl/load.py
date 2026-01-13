import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_USER = "payroll_app"
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "payroll_db"

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

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
