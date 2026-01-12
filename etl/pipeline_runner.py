import os
from etl.extract import extract_payroll
from etl.transform import transform_payroll

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"

# Ensure processed folder exists
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def run_pipeline():
    # Loop over all CSV files in raw folder
    for filename in os.listdir(RAW_FOLDER):
        if filename.endswith(".csv"):
            file_path = os.path.join(RAW_FOLDER, filename)
            print(f"\nProcessing file: {filename}")

            # Extract
            df_raw = extract_payroll(file_path)

            # Transform
            df_transformed = transform_payroll(df_raw)

            # Preview transformed data
            print(df_transformed.head())

            # Save processed data
            processed_file_path = os.path.join(PROCESSED_FOLDER, filename)
            df_transformed.to_csv(processed_file_path, index=False)
            print(f"Saved transformed file to: {processed_file_path}")

if __name__ == "__main__":
    run_pipeline()
