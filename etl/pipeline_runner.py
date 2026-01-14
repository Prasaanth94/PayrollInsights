import os
from etl.extract import extract_payroll
from etl.transform import transform_payroll
from etl.load import load_to_mysql
from etl.signals import update_payroll_signals
from etl.risk_scoring_agent import run_payroll_agent
from etl.risk_action_agent import run_risk_agent

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"

# Ensure processed folder exists
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def run_pipeline(test_file=None):

    files_to_process = [test_file] if test_file else os.listdir(RAW_FOLDER)

    # Loop over all CSV files in raw folder
    for filename in files_to_process:
        if filename.endswith(".csv"):
            file_path = os.path.join(RAW_FOLDER, filename)
            print(f"\nProcessing file: {filename}")

            # Extract
            df_raw = extract_payroll(file_path)

            # Transform
            df_transformed = transform_payroll(df_raw)
            print("Transformed Data preview")
            print(df_transformed.head())

            # Save processed data
            processed_file_path = os.path.join(PROCESSED_FOLDER, filename)
            df_transformed.to_csv(processed_file_path, index=False)
            print(f"Saved transformed file to: {processed_file_path}")

            #load into MySql
            print("Loading into MySql...")
            load_to_mysql(processed_file_path)

            #update payroll signals
            print("Updating payroll signals")
            update_payroll_signals()
            print("Signals updated Successfully")

            #Agent review
            print("Agent reviewing")
            run_payroll_agent()
            print("Agent review successful")

            #Agent actions
            print("Agent working on actions")
            run_risk_agent()
            print("Agent actions made.")

if __name__ == "__main__":
    run_pipeline()
