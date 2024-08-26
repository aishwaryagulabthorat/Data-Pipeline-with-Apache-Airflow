from airflow.decorators import dag,task  ##decorators are used for taskAPI
from datetime import datetime

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator


from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType
from airflow.operators.python import PythonOperator

from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig #ProjectConfig, 

from airflow.models.baseoperator import chain

@dag(
    start_date=datetime(2024,8,21),
    schedule=None, #we are going to run it manually
    catchup=False, # we do not want to run all past not triggered dag runs
    tags=['retail'], #simply giving a tag to our DAG
)

def retail():
    #TASK1 -> To save the csv file from out local machione to the GCP bucket we created

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',            #id of the task
        src='include/dataset/Online_Retail.csv', #source of the file we want to upload
        dst='raw/online_retail.csv',                #destination in the GCS bucket
        bucket='aishthorat_online_retail',        #bucket name
        gcp_conn_id='GCP',                      # use the conn_id used in GCP while creating a connection
        mime_type='text/csv',                   #type of the file
    )

    #once you create a task run - astro dev bash - in terminal to access the container 
    #then run - airflow tasks test dag_id(retail) task_id executiondate(2024-8-21)
    #make sure whenever you test your tasks you should be in /usr/local/airflow folder

    # Task2-> Create an empty dataset in bigquery 

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='GCP',
    )
    #again test the task


    #TASK3 -> now load the data from csv file present in bucket into a bigquery table raw_invoices

    
    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(   #it will take three parameters
            'gs://aishthorat_online_retail/raw/online_retail.csv', #path of the bucket where you saved the CSV file
            # '{{ task_instance.xcom_pull(task_ids="preprocess_csv_task") }}',  # the path of the preprocessed file in GCS
            conn_id='GCP',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices', #name of the bigquery table you want to get created
            conn_id='GCP',
            metadata=Metadata(schema='retail') # name of the empty dataset you created
        ),
        use_native_support=False,
    )
    #again test the task

    #TASK4 -> do the quality check using soda

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    #we will use external python decorator/operator that allows you to run python code within precreated python
    #virtual environment

    #test the task - now that we have used external python operator @task.external_python to create
    # this task we will have to call this task explicitly

    # check_load() #we added in chain so remove calling function

    #TASK 5 -> To tranform the data from retail into data models dim and fact tables

    transform = DbtTaskGroup(       #each dbt model will be a task
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG, #using DBT_PROJECT_CONFIG from cosmos.py
        profile_config=DBT_CONFIG,          #using DBT_CONFIG from cosmos.py
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        ))

    #TASK 6 -> Data Quality checks on fact and dimension tables

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    #we will use external python decorator/operator that allows you to run python code within precreated python
    #virtual environment

    #test the task - now that we have used external python operator @task.external_python to create
    # this task we will have to call this task explicitly

    # check_transform() #we added in chain so remove calling function

    report = DbtTaskGroup(       #each dbt model will be a task
        group_id='report',
        project_config=DBT_PROJECT_CONFIG, #using DBT_PROJECT_CONFIG from cosmos.py
        profile_config=DBT_CONFIG,          #using DBT_CONFIG from cosmos.py
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        ))
    

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='report'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    #we will use external python decorator/operator that allows you to run python code within precreated python
    #virtual environment

    #test the task - now that we have used external python operator @task.external_python to create
    # this task we will have to call this task explicitly

    # check_report() #we added in chain so remove calling function

    chain(
        upload_csv_to_gcs,
        create_retail_dataset,
        gcs_to_raw,
        check_load(),
        transform,
        check_transform(),
        report,
        check_report() 

    )

retail()






