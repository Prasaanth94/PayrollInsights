import pandas as pd
from sqlalchemy import text
from db.engine import engine

def load_to_mysql(file_path: str):
    """
    Load a CSV file into the 'payroll' table in MySQL.
    Only inserts rows if the (employee_id, pay_period) combination doesn't exist.
    """
    print(f"Loading {file_path} into MySQL...")
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO payroll (
                    employee_id, employee_name, department, role,
                    base_salary, overtime_pay, net_pay, calculated_net_pay,
                    salary_change_pct, has_salary_change, pay_period, gross_pay
                )
                VALUES (
                    :employee_id, :employee_name, :department, :role,
                    :base_salary, :overtime_pay, :net_pay, :calculated_net_pay,
                    :salary_change_pct, :has_salary_change, :pay_period, :gross_pay
                )
                ON DUPLICATE KEY UPDATE
                    employee_name = VALUES(employee_name),
                    department = VALUES(department),
                    role = VALUES(role),
                    base_salary = VALUES(base_salary),
                    overtime_pay = VALUES(overtime_pay),
                    net_pay = VALUES(net_pay),
                    calculated_net_pay = VALUES(calculated_net_pay),
                    salary_change_pct = VALUES(salary_change_pct),
                    has_salary_change = VALUES(has_salary_change),
                    gross_pay = VALUES(gross_pay)
            """), row.to_dict())
    
    print(f"Successfully loaded {len(df)} rows into MySQL.")
