# Data-Pipeline-with-Apache-Airflow-GCP

This repository contains a data pipeline built using Apache Airflow using Astro CLI. The pipeline automates the processing of an online retail dataset, ensuring data quality and preparing it for reporting in Metabase.

# Complete Flow

<img width="1374" alt="image" src="https://github.com/user-attachments/assets/6a5abfc8-ddf2-4f8e-8fa7-df368e3f556c">

# The key components of the pipeline are:

## Pipeline Overview
1. **Data Ingestion**:             The pipeline starts by ingesting raw data from a CSV file containing online retail transactions.
2. **Quality Checks**:             After ingestion, SODA is used to run quality checks on the raw dataset to ensure its integrity before proceeding to the transformation stage.
3. **Transformation**:             The raw data is transformed using dbt models. These models are used to clean, structure, and enrich the dataset, preparing it for further analysis.

After the transformation step using dbt models, the raw data is structured into a star schema to optimize it for analytical queries.
The schema consists of the following tables:

Fact Table:
  - fct_invoices

Dimension Tables:
  - dim_product
  - dim_customer
  - dim_datetime

<img width="699" alt="image" src="https://github.com/user-attachments/assets/3405502e-66a1-4f9c-abf3-5f8b0c7246ed">

This star schema simplifies querying for reports and analytics by organizing data into a clear and efficient structure, allowing for easy aggregation and slicing of data across different dimensions like time, product, and customer.

4. **Quality Checks on Transformed Data**: Post-transformation, additional quality checks are performed to ensure the data's accuracy and reliability.
5. **Reporting**:                          After the data passes all quality checks, it is prepared for reporting.
6. **Metabase Integration**:               The processed data is made available for visualization and analysis in Metabase.

## Tools and Technologies Used

- **Apache Airflow**:                     Workflow orchestration
- **Astro CLI**:                          Local development of the Airflow pipeline
- **SODA**:                               Data quality checks
- **dbt**:                                Data transformation
- **Metabase**:                           Data visualization and reporting

## Future Enhancements

Expanding quality checks with additional rules and validations.

Incorporating more data sources for a comprehensive data analysis.

Optimization of dbt models for performance improvements.



Project Contents
================

Project contains the following files and folders:

- dags: This folder contains the Python file retail.py with all the tasks for Airflow DAG. 
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. And it also contains code to create a python virtual environment to install soda and dbt.
- include: This folder contains folders for dataset, dbt, GCP, metabase-data and soda.
- packages.txt: Install OS-level packages needed for the project by adding them to this file.
- requirements.txt: Install Python packages and cosmos needed for the project.
- airflow_settings.yaml: local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as DAGs are developed in this project.

Deploy Project Locally
===========================

1. Start Airflow on local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

3. Access the Airflow UI for local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

Should also be able to access Postgres Database at 'localhost:5432/postgres'.
