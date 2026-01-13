import os
from sqlalchemy import create_engine, text  # <-- import text
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
engine = create_engine(f"mysql+mysqlconnector://payroll_app:{DB_PASSWORD}@localhost/payroll_db")

try:
    with engine.connect() as conn:
        # Wrap SQL string in text()
        result = conn.execute(text("SHOW TABLES;"))
        print("Tables in payroll_db:", [row[0] for row in result])
except Exception as e:
    print("Connection failed:", e)
