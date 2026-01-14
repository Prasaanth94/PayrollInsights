import os
import pandas as pd

PROCESSED_FOLDER = "data/processed"

def check_net_pay():
    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith(".csv"):
            file_path = os.path.join(PROCESSED_FOLDER, filename)
            df = pd.read_csv(file_path)

            #calculate net pay
            df["calculated_net_pay"] = df["base_salary"] + df["overtime_pay"] + df["bonus"] - df["deductions"]


            #compare with existing netpay
            mismatches = df[df["net_pay"] != df["calculated_net_pay"]]

            print(f"\nFile: {filename}")
            if mismatches.empty:
                print("All net_pay values match calculated_net_pay")
            else:
                print("Mismatches found:")
                print(mismatches)

if __name__ == "__main__":
    check_net_pay()
            