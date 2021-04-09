# MDWProfiler

**This repo contains Python scripts to generate data profiles for the auto-classification and matching of data-classes and data-elements to the NHS Data Dictionary.**

## Table of contents

1. [Data Sources](#)
2. [Setting up the Tool]

## Data Sources
#data-sources

| DATA TYPE  | DETAILS | SCRIPTS |
| ---        | --- | --- |
| Flat Text Files | Text files, CSV, TSV, or other separators | <code>profile_text.py</code> <code>requirements_text.txt</code> <code>pandas_profiler_config_mdw.yaml</code>|
| Excel Files | The profiler treats every worksheet as its own dataclass | <code>profile_excel.py</code> <code>requirements_excel.txt</code> <code>pandas_profiler_config_mdw.yaml</code>|
| Relational Databases | The script will profile all tables in a given RDBMS schema | <code>profile_mysql.py</code> <code>requirements_mysql.txt</code> <code>pandas_profiler_config_mdw.yaml</code>|


## Setting up the Tool

To set up project:
1. Create a new virtual environment using venv:

<code>python3 -m venv venv</code>

2. Activate virtual environment

<code>source venv/bin/activate</code>

3. Install requirements from requirements.txt

<code>pip install -r requirements.txt</code>