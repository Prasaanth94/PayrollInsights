import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

PROCESSED_FOLDER = "data/processed"

load_dotenv()

DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "payroll_insights"

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

def load_to_mysql():
    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith(".csv"):
            file_path = os.path.join(PROCESSED_FOLDER, filename)
            df = pd.read_csv(file_path)


            print(f"Loading {filename} into Mysql...")
            df.to_sql(
                name="payroll",
                con=engine,
                if_exists="append",
                index=False
            )

    print("Data loaded successfully")

if __name__ == "__main__":
    load_to_mysql()        