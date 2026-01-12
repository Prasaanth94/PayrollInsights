import pandas as pd

def transform_payroll(df: pd.DataFrame) -> pd.DataFrame:
    #convert pay_period to full date(json friendly)
    df["pay_period"] = pd.to_datetime(df["pay_period"], format="%Y-%m")
    df["pay_period"] = df["pay_period"].dt.strftime("%Y-%m-%d")

    #calculate gross pay
    df["gross_pay"]  = df["base_salary"] + df["overtime_pay"] + df["bonus"]

    #calculate net pay
    df["calculated_net_pay"] = df["gross_pay"] - df["deductions"]

    #calculate salary change % compared to previous month
    df = df.sort_values(by=["employee_id", "pay_period"])
    df["salary_change_pct"] = df.groupby("employee_id")["base_salary"].pct_change().fillna(0) * 100
    
    #add boolean flag if base_salary changed
    df["has_salary_change"] = df["salary_change_pct"].apply(lambda x: x !=0)

    df["net_pay"] = df["gross_pay"] - df["deductions"]

    df["role"] = df["role"].str.title()

    return df