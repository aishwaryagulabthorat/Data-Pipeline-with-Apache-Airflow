<<<<<<< HEAD
Overview
========

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
    - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.
=======
# Data-Pipeline-with-Apache-Airflow

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
>>>>>>> origin/main
