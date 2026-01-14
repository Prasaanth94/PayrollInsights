import csv
import random
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta

# ---------------- Configuration ----------------
NUM_EMPLOYEES = 10
NUM_MONTHS = 3
ANOMALY_CHANCE = 0.3  # random anomaly probability

DEPARTMENTS = ["Engineering", "Sales", "HR", "Finance", "Marketing"]
ROLES = {
    "Engineering": ["Software Engineer", "DevOps Engineer", "Data Analyst"],
    "Sales": ["Account Manager", "Sales Rep", "Team Leader"],
    "HR": ["HR Specialist"],
    "Finance": ["Accountant", "Finance Analyst"],
    "Marketing": ["Marketing Specialist", "Content Creator"]
}

SALARY_RANGE = (3000, 8000)
OVERTIME_RANGE = (0, 1000)
BONUS_RANGE = (0, 500)
DEDUCTIONS_RANGE = (300, 500)

OUTPUT_DIR = "data/raw"
SAMPLE_CSV = "sample_data/payroll_sample.csv"

# ---------------- Functions ----------------

def random_employee(emp_id):
    dept = random.choice(DEPARTMENTS)
    role = random.choice(ROLES[dept])
    name = f"Employee_{emp_id}"
    return {"employee_id": emp_id, "employee_name": name, "department": dept, "role": role}


def generate_payroll_for_employee(emp, base_salary_prev=None, force_anomaly=False):
    # Base salary
    if base_salary_prev is None:
        base_salary = random.randint(*SALARY_RANGE)
    else:
        if random.random() < 0.05:
            base_salary = int(base_salary_prev * (1 + random.uniform(0, 0.03)))
        else:
            base_salary = base_salary_prev        

    # Other components
    overtime = random.randint(*OVERTIME_RANGE)
    bonus = random.randint(*BONUS_RANGE)
    deductions = random.randint(*DEDUCTIONS_RANGE)

    # Inject anomalies (forced or random)
    if force_anomaly or (base_salary_prev and random.random() < ANOMALY_CHANCE):
        anomaly_type = "SALARY_SPIKE" if force_anomaly else random.choice(
            ["SALARY_SPIKE", "OVERTIME_SURGE", "MISSING_DEDUCTION", "BONUS_OUTLIER"]
        )
        if anomaly_type == "SALARY_SPIKE":
           if base_salary_prev is not None:
                base_salary = int(base_salary_prev * 1.25)
           else:
                base_salary = random.randint(int(SALARY_RANGE[1]*0.9), SALARY_RANGE[1])
        elif anomaly_type == "OVERTIME_SURGE":
            overtime = int(overtime * 1.6 + 100)
        elif anomaly_type == "MISSING_DEDUCTION":
            deductions = 0      
        elif anomaly_type == "BONUS_OUTLIER":   
            bonus = BONUS_RANGE[1] + 100

    net_pay = base_salary + overtime + bonus - deductions
    return {
        **emp,
        "base_salary": base_salary,
        "overtime_pay": overtime,
        "bonus": bonus,
        "deductions": deductions,
        "net_pay": net_pay
    }

# ---------------- Main Script ----------------

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("sample_data", exist_ok=True)

    # Generate employees
    employees = [random_employee(emp_id) for emp_id in range(1, NUM_EMPLOYEES + 1)]

    # Pick 2 employees to have guaranteed anomalies
    guaranteed_anomalies = random.sample(employees, 2)

    start_month = datetime.strptime("2026-01", "%Y-%m")
    all_rows = []

    # Generate payroll month by month
    for month_idx in range(NUM_MONTHS):
        month_date = start_month + relativedelta(months=month_idx)
        pay_period = month_date.strftime("%Y-%m")
        month_rows = []

        for emp in employees:
            # Find previous month's base salary
            prev = None
            for r in all_rows:
                if r["employee_id"] == emp["employee_id"]:
                    prev = r
            base_prev = prev["base_salary"] if prev else None

            # Force anomaly if employee is in guaranteed list
            force_anomaly = emp in guaranteed_anomalies

            payroll_row = generate_payroll_for_employee(emp, base_prev, force_anomaly)
            payroll_row["pay_period"] = pay_period
            month_rows.append(payroll_row)

        # Save monthly CSV
        month_file = f"{OUTPUT_DIR}/payroll_{pay_period}.csv"
        with open(month_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=month_rows[0].keys())
            writer.writeheader()
            writer.writerows(month_rows)

        all_rows.extend(month_rows)

    # Save small sample CSV for repo
    sample_rows = all_rows[:5]
    with open(SAMPLE_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sample_rows[0].keys())
        writer.writeheader()
        writer.writerows(sample_rows)

    print(f"Payroll CSVs generated in {OUTPUT_DIR}")
    print(f"Sample CSV saved at {SAMPLE_CSV}")
    print("Guaranteed anomalies added for employees:", [e["employee_id"] for e in guaranteed_anomalies])


if __name__ == "__main__":
    main()
