from sqlalchemy import text
from db.engine import engine
from etl.alerts import send_alert
import pandas as pd

def run_risk_agent():
    print(("Running Payroll risk agent"))

    high_risk_employees = []

    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT
                employee_id,
                pay_period,
                net_pay_mismatch,
                high_overtime_flag,
                low_net_pay_flag,
                department_deviation_pct,
                salary_spike_flag,
                low_net_pay_flag
            FROM payroll_signals                                      
        """))

        for row in result:
            score = 0
            reasons = []

            if row.net_pay_mismatch == 1:
                score += 40
                reasons.append("Net pay mismatch")

            if row.salary_spike_flag == 1:
                score += 40
                reasons.append("Salary spike")    

            if row.high_overtime_flag == 1:
                score += 25
                reasons.append("High overtime")    

            if row.low_net_pay_flag == 1:
                score += 20
                reasons.append("Low net pay vs department")

            if abs(row.department_deviation_pct or 0) > 30:
                score += 15
                reasons.append("High deviation from department avg")    

            if score >= 60:
                level = "HIGH"
            elif score >= 30 :
                level = "MEDIUM"
            else:
                level = "LOW"

            conn.execute(text("""
            INSERT INTO payroll_risk_scores
            (employee_id, pay_period, risk_score, risk_level, reasons)
            VALUES (:eid, :pp, :score, :level, :reasons)
            ON DUPLICATE KEY UPDATE
                risk_score = VALUES(risk_score),
                risk_level = VALUES(risk_level),
                reasons = VALUES(reasons)        
                                                
            """), {
                "eid" : row.employee_id,
                "pp" : row.pay_period,
                "score" : score,
                "level" : level,
                "reasons" : ", ".join(reasons)
            })  

            if level == "HIGH":
                high_risk_employees.append({
                    "employee_id" : row.employee_id,
                    "pay_period" : row.pay_period,
                    "risk_score" : score
                })          

    

            if high_risk_employees:
                subject = "Payroll Risk Alert: High-Risk Employees Detected"
                body = "The Following employees have HIGH payroll Risk: \n\n"
                for emp in high_risk_employees():
                    body += f"Employee_id: {row['employee_id']}, Pay Period: {row['pey_period']}, Risk ScoreL:{row['risk_score']}\n"
                send_alert(subject,body)    

    print("Risk Agent completed.")