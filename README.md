# MDWProfiler

This repo contains Python scripts to generate data profiles for the auto-classification and matching of data-classes and data-elements to the NHS Data Dictionary.

# Table of contents

1. [Data Sources](# data-sources)
2. [Flat Text Files](# flat-text-files)
3. [Excel Files](# excel-files)

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

| Parameter | Description | Default |
| --- | --- | --- |
| <code>DATA_PATH</code> | The path to the text files to be profiled | 'current working directory'\data | 
| <code>PROFILE_PATH</code> | The path to which the profile for each data class is written | 'current working directory'\profile |
| <code>SEPARATOR</code> | The separator used in the data files, such as CSV, TSV, and any others | , |
| <code>ROW_LIMIT</code> | This limits the number of rows to be profiled, for performance reasons, please set to 0 to read all rows | 10000 |

## Requirements
Python packages required to run the profiler, they can also be found in the requirements_text.txt file: <br/>
<code>Python 3.7</code><br/>
<code>pandas==1.2.3</code><br/>
<code>pandas_profiling==2.11.0</code><br/>
<code>requests==2.25.1</code>


## Setting up the Tool

To set up project:
1. Create a new virtual environment using venv:

<code>python3 -m venv venv</code>

2. Activate virtual environment

<code>source venv/bin/activate</code>

3. Install requirements from requirements.txt<br/>
Re-name file requirements_text.txt to requirements.txt

<code>pip install -r requirements.txt</code>


# Excel Files

This profiler reads an Excel data file. Each worksheet is treated as a data class. The resulting profile will be written to a profile path or directory in JSON format.

## Required Repo Files

| File | Description |
| --- | --- |
| <code>profile_excel.py</code> | This file contains the Python code to run the profiler on Excel files |
| <code>requirements_excel.txt</code> | Please change the name to <code>requirements.txt</code> to set up your virtual environment |
| <code>pandas_profiler_config_mdw.yaml</code> | This file contains the profiler configuration |

## Parameters

These are the parameters to set up for <code>profile_text.py</code>

| Parameter | Description | Default |
| --- | --- | --- |
| <code>DATA_PATH</code> | The path to the text files to be profiled | 'current working directory'\data | 
| <code>PROFILE_PATH</code> | The path to which the profile for each data class is written | 'current working directory'\profile |
| <code>FILES</code> | A list of excel filename to be profiled, this is a required parameter |  |

## Requirements
Python packages required to run the profiler, they can also be found in the requirements_text.txt file: <br/>
<code>Python 3.7</code><br/>
<code>pandas==1.2.3</code><br/>
<code>pandas_profiling==2.11.0</code><br/>
<code>requests==2.25.1</code>


## Setting up the Tool

To set up project:
1. Create a new virtual environment using venv:

<code>python3 -m venv venv</code>

2. Activate virtual environment

<code>source venv/bin/activate</code>

3. Install requirements from requirements.txt<br/>
Re-name file requirements_text.txt to requirements.txt

<code>pip install -r requirements.txt</code>


# License

MIT License

Copyright (c) 2021 MetadataWorks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.