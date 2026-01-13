import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def update_payroll_signals():
    #connect to my sql
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = os.getenv("MYSQL_PASSWORD"),
        database = "payroll_db"
    ) 

    cursor = conn.cursor()

    try:
        # 1 Net pay mismatch
        cursor.execute("""
            UPDATE payroll_signals s
            JOIN payroll p
              ON s.employee_id = p.employee_id
             AND s.pay_period = p.pay_period
            SET s.net_pay_mismatch = ABS(p.net_pay - p.calculated_net_pay) > 0.01
            WHERE s.employee_id IS NOT NULL;
        """)

        # 2 Overtime ratio
        cursor.execute("""
            UPDATE payroll_signals s
            JOIN payroll p
              ON s.employee_id = p.employee_id
             AND s.pay_period = p.pay_period
            SET s.overtime_ratio = ROUND(p.overtime_pay / NULLIF(p.base_salary, 0), 2)
            WHERE s.employee_id IS NOT NULL;
        """)

        # 3 Department deviation percentage
        cursor.execute("""
            UPDATE payroll_signals s
            JOIN payroll p
              ON s.employee_id = p.employee_id
             AND s.pay_period = p.pay_period
            JOIN (
                SELECT department, pay_period, AVG(net_pay) AS dept_avg
                FROM payroll
                GROUP BY department, pay_period
            ) d
              ON p.department = d.department
             AND p.pay_period = d.pay_period
            SET s.department_deviation_pct = ROUND((p.net_pay - d.dept_avg) / d.dept_avg * 100, 2)
            WHERE s.employee_id IS NOT NULL;
        """)

        

        # Commit all changes
        conn.commit()
        print("Payroll signals updated successfully.")

    except mysql.connector.Error as err:
        print("Error updating payroll signals:", err)
        conn.rollback()  # rollback in case of error

    finally:
        cursor.close()
        conn.close()