# MDWProfiler
MetadataWorks Profiler

## Data Sources
* Flat text files (CSV, TSV, or other separators)
* Excel files
* Profile data such as SPSS, White Rabbit
* Relational databases (MySQL, PostGres)


## How the repo is organised

### Config

Contains the code variables and paramteres (explain each file briefly)

### Utils

Contains utility functions and scripts to support the tooling (explain each file briefly)

### Data

How should we organise this?  What goes in it?


## Setting up the Tool

To set up project:
1. Create a new conda virtual environment:

<code>conda create --mdwprofiler python=3.9</code>

2. Activate virtual environment

<code>conda activate mdwprofiler</code>

3. Install requirements from requirements.txt

<code>pip install -r requirements.txt</code>


## Setting up the required directories

Run the following commands in terminal:

<code>mkdir lcl_data</code><br>
<code>cd lcl_data</code><br>
<code>mkdir text</code><br>
<code>cd text</code><br>
<code>mkdir data</code><br> 
<code>mkdir pandas_profiles</code><br> 
