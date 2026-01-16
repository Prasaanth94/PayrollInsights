from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from etl.pipeline_runner import run_pipeline


default_args = {
    "owner" : "data-engineering",
    "depends_on_past" : False,
    "retries" : 1
}



with DAG_(
    dag_id = "payroll_agentic_pipeline",
    description = "End-to-end payrol risk detection and alerting pipeluine",
    default_args=default_args,
    start_date = datetime(2025,1,1),
    schedule_interval = "@monthly",
    catchup = False,
    tags = ["payroll", "risk", "agentic-ai"]
) as dag:
    
    run_payrol_pipiline = PythonOperator(
        task_id = "run_payroll_pipeline",
        python_callable = run_pipeline
    )

    run_payrol_pipiline