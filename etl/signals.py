from sqlalchemy import text
from db.engine import engine



def update_payroll_signals():
    print("Updating payroll signals...")


    with engine.begin() as conn:
        #ensure base rows exist
        conn.execute(text("""
            INSERT IGNORE INTO payroll_signals (employee_id, pay_period)
            SELECT employee_id, pay_period
            FROM payroll;              
        """))

         #net pay mismatch
        conn.execute(text("""
            UPDATE payroll_signals s
            JOIN payroll p
            ON s.employee_id = p.employee_id
            AND s.pay_period = p.pay_period
            SET s.net_pay_mismatch =
                ABS(p.net_pay - p.calculated_net_pay) > 0.01;              
            
         """))
        
        #over time ratio
        conn.execute(text("""
            UPDATE payroll_signals S
            JOIN payroll p
            ON s.employee_id = p.employee_id
            AND s.pay_period = p.pay_period
            SET s.overtime_ratio =
                ROUND(p.overtime_pay / NULLIF(p.base_salary, 0), 2);

        """))

        # Department deviation %
        conn.execute(text("""
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
            SET s.department_deviation_pct =
                ROUND((p.net_pay - d.dept_avg) / d.dept_avg * 100, 2);
        """))

        #high over time flag
        conn.execute(text("""
        UPDATE payroll_signals
        SET high_overtime_flag = CASE
            WHEN overtime_ratio > 0.30 THEN 1
            ELSE 0
        END;                  
        """))

        #salary spike flag
        conn.execute(text("""
        UPDATE payroll_signals s
        JOIN payroll p
        ON s.employee_id = p.employee_id
        AND s.pay_period = p.pay_period
        SET s.salary_spike_flag =
            CASE
                WHEN p.salary_change_pct > 20 THEN 1
                ELSE 0
            END
        """))

        #low net pay anomaly
        conn.execute(text("""
        UPDATE payroll_signals s
        JOIN payroll p
        on s.employee_id = p.employee_id
        AND s.pay_period = p.pay_period
        JOIN (
            SELECT department, pay_period, AVG(net_pay) AS dept_avg
            FROM payroll
            GROUP BY department, pay_period
        )d
          ON p.department = d.department
          AND p.pay_period - d.pay_period
          SET s.low_net_pay_flag =
            CASE
                WHEN p.net_pay < d.dept_avg * 0.75 THEN 1
                ELSE 0
            END;              

        """))

    print("Payroll signals updated successfully.")
   