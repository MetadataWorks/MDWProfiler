# MDWProfiler

This repo contains Python scripts to generate data profiles for the auto-classification and matching of data-classes and data-elements to the NHS Data Dictionary.

# Table of contents

1. [Data Sources](#-data-sources)
2. [Flat Text Files](#-flat-text-files)

# Data Sources

| DATA TYPE  | DETAILS | SCRIPTS |
| ---        | --- | --- |
| Flat Text Files | Text files, CSV, TSV, or other separators | <code>profile_text.py</code> <code>requirements_text.txt</code> <code>pandas_profiler_config_mdw.yaml</code>|
| Excel Files | The profiler treats every worksheet as its own dataclass | <code>profile_excel.py</code> <code>requirements_excel.txt</code> <code>pandas_profiler_config_mdw.yaml</code>|
| Relational Databases | The script will profile all tables in a given RDBMS schema | <code>profile_mysql.py</code> <code>requirements_mysql.txt</code> <code>pandas_profiler_config_mdw.yaml</code>|


# Flat Text Files

This profiler reads all text files in a given path or directory. Each file is treated as a data class. The resulting profile will be written to a profile path or directory in JSON format.

## Required Repo Files

| File | Description |
| --- | --- |
| <code>profile_text.py</code> | This file contains the Python code to run the profiler on text data |
| <code>requirements_text.txt</code> | Please change the name to <code>requirements.txt</code> to set up your virtual environment |
| <code>pandas_profiler_config_mdw.yaml</code> | This file contains the profiler configuration |

## Parameters

These are the parameters to set up for <code>profile_text.py</code>

| 

## Setting up the Tool

To set up project:
1. Create a new virtual environment using venv:

<code>python3 -m venv venv</code>

2. Activate virtual environment

<code>source venv/bin/activate</code>

3. Install requirements from requirements.txt

<code>pip install -r requirements.txt</code>


# License
This codebase is made available under a [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.