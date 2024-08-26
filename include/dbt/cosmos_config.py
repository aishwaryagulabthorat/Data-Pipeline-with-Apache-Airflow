from cosmos.config import ProfileConfig, ProjectConfig
from pathlib import Path

DBT_CONFIG = ProfileConfig(   #what profile you want to use
    profile_name='retail',
    target_name='dev',
    profiles_yml_filepath=Path('/usr/local/airflow/include/dbt/profiles.yml')
)

DBT_PROJECT_CONFIG = ProjectConfig(         #specifies where the dbt project is
    dbt_project_path='/usr/local/airflow/include/dbt/',
)