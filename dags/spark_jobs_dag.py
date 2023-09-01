import airflow
from datetime import timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',    
    'retry_delay': timedelta(minutes=5),
}

jar_path = "/opt/airflow/jars/"

spark_dag = DAG(
        dag_id = "spark_airflow_dag",
        default_args=default_args,
        schedule_interval=None,	
        dagrun_timeout=timedelta(minutes=60),
        description='use case of sparkoperator in airflow',
        start_date = airflow.utils.dates.days_ago(1)
)

Extract = SparkSubmitOperator(
		application = "/opt/airflow/dags/spark_etl_script_docker.py",
		conn_id= 'spark_local', 
		task_id='spark_submit_task', 
        jars=jar_path+"hadoop-azure-3.2.0.jar,"+jar_path+"hadoop-azure-datalake-3.2.1.jar,"+jar_path+"azure-storage-8.6.3.jar,"+jar_path+"wildfly-openssl-2.0.0.Alpha1.jar",
        dag=spark_dag
		)

Extract