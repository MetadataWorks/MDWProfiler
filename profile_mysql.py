import datetime
import os
import platform
import mysql.connector
import pandas as pd
import pandas_profiling as pp
import requests
import json

DB_CONNECTION = {'host':'please enter your db host',
                 'user':'please enter your db user-name',
                 'passwd':'please enter your db password',}
DB_SCHEMA = 'please enter your db schema'
SQL_LIMIT = 20000
EXCLUDE_TABLES = []
CWD = os.getcwd()
PROFILE_PATH = os.path.join(CWD, 'lcl_data', 'profiles')
__version__ = '20210517'


def main():
    write_header()

    # connect to the database
    db_connection = connect_to_db(DB_CONNECTION)
    ddic = read_mysql_ddic(db_connection, DB_SCHEMA, EXCLUDE_TABLES)
    pd_profile = generate_pandas_profile(db_connection, DB_SCHEMA, ddic, SQL_LIMIT)
    write_pandas_profile(os.path.join(CWD, PROFILE_PATH), pd_profile, SQL_LIMIT)

    db_connection.close()
    write_timestamp(f"done")
    return


def connect_to_db(db_config):
    db = None
    try:
        db = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return None, None
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return None, None
        else:
            print(err)
            return None, None

    print()
    return db


def generate_pandas_profile(db_connection, db_schema, ddic, limit):
    profile = []
    all_keys = []

    for db_table, db_tbdef in ddic.items():
        db_table_def = ddic.get(db_table, {})
        write_timestamp(f" - database table '{db_schema}.{db_table}'")
        if limit > 0:
            sql_statement = f"SELECT * FROM `{db_schema}`.`{db_table}` LIMIT {limit};"
        else:
            sql_statement = f"SELECT * FROM `{db_schema}`.`{db_table}`;"
        df = sql_select_to_pd(db_connection, sql_statement)

        write_timestamp(f"   start profile for {len(df)} rows")
        table_profile = pp.ProfileReport(df,
                                         title=f"Profile {db_table}",
                                         config_file='pandas_profiler_config_mdw.yaml',
                                         dark_mode=True)
        write_timestamp(f"   convert to JSON")
        string_profile = table_profile.to_json()
        json_profile = json.loads(string_profile)
        dbtab_profile = {"data_class_name": db_table,
                         "data_class_features": {"db table": f"{db_schema}.{db_table}"}}
        for key, value in json_profile.get('table', {}).items():
            if key in ['n', 'n_var', 'n_cells_missing', 'n_vars_with_missing', 'n_duplicates']:  # , 'types']:
                dbtab_profile["data_class_features"][key] = value
        dbtab_profile["data_elements"] = []
        for de_name, de_data in json_profile.get('variables', {}).items():
            db_column_def = db_table_def.get(de_name, {})
            de_profile = {'data_element_name': de_name,
                          'data_type': db_column_def.get('data_type', ''),
                          'data_element_features': {}}
            for de_key, de_value in de_data.items():
                all_keys.append(de_key)
                if de_key in ['count', 'n_distinct', 'is_unique', 'n_missing', 'count', 'mean', 'std',
                              'variance', 'min', 'max', 'range', '5%', '25%', '50%', '75%', '95%', 'n_category',
                              'value_counts_without_nan']:
                    if 'value_counts_without_nan' == de_key:
                        if len(de_value.keys()) < 33:
                            de_profile['data_element_features'][de_key] = de_value
                    else:
                        de_profile['data_element_features'][de_key] = de_value
            dbtab_profile["data_elements"].append(de_profile)
        profile.append(dbtab_profile)

    all_keys = list(set(all_keys))
    all_keys.sort()
    print()
    return profile


# timestamp
def write_timestamp(out_text=''):
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f"{now} {out_text}")
    return


def write_header():
    write_timestamp(f"{__file__}")
    print(f"python=={platform.python_version()}")
    print(f"mysql.connector=={mysql.connector.__version__}")
    print(f"pandas=={pd.__version__}")
    print(f"pandas_profiling=={pp.__version__}")
    print(f"requests=={requests.__version__}")
    print()


def read_mysql_ddic(db_connection, db_schema, exclude_tables):
    write_timestamp(f"read data dictionary for {db_schema}")
    dtypes = {'bigint': 'integer',
              'bit': 'integer',
              'datetime': 'datetime',
              'decimal': 'float',
              'double': 'float',
              'int': 'integer',
              'longtext': 'text',
              'tinyint': 'integer',
              'varchar': 'text', }
    read_schema = db_schema.replace('`', '')
    ddic = {}
    sql_statement = f"SELECT DISTINCT c.table_name AS table_name, c.column_name AS column_name, c.ordinal_position AS ordinal_position, " \
                    f"c.data_type AS data_type, c.column_type AS column_type, c.column_key AS column_key, c.extra AS extra " \
                    f"FROM information_schema.TABLES AS t INNER JOIN information_schema.COLUMNS AS c ON t.TABLE_NAME = c.TABLE_NAME " \
                    f"WHERE t.table_schema = '{read_schema}' AND t.table_type = 'BASE TABLE' ORDER BY c.table_name , c.ORDINAL_POSITION;"
    sql_result = sql_select_to_json(db_connection, sql_statement)

    if len(sql_result) < 1:
        print()
        return ddic

    for sr in sql_result:
        table_name = sr['table_name']
        if table_name in exclude_tables:
            continue
        if not ddic.get(table_name, None):
            ddic[table_name] = {}
        ddic[table_name][sr['column_name']] = {'data_type': dtypes.get(sr['data_type'], sr['data_type']),
                                               'db_type': sr['column_type'],
                                               'position': sr['ordinal_position'],
                                               'primary_key': (True if 'PRI'==sr['column_key'] else False),
                                               'linkable': sr['column_key'],
                                               'db_ddic': sr,}
    print()
    return ddic


def sql_select_to_pd(db, sql_statement):
    sql_select = None
    try:
        sql_select = pd.read_sql(sql_statement, con=db)
    except Exception as e:
        write_timestamp(f"SQL select error")

    return sql_select


def sql_select_to_json(db, sql_statement):
    json_select = None
    df_select = sql_select_to_pd(db, sql_statement)
    try:
        json_select = df_select.to_dict(orient='records')
    except Exception as e:
        write_timestamp(f"{e}")
    return json_select


def export_json(data, filename, indent=2):
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=indent)
        return


def write_pandas_profile(profile_path, profile, limit):
    if len(profile) < 1:
        return
    json_out = {"mdw_profiler": "relational database",
                "version": __version__,
                "profile_timestamp": datetime.datetime.now().strftime("%Y%m%dT%H%M%S"),
                "profiler_configuration": {"rdbms": "MySQL",
                                           "row_limit": limit,
                                           "redaction": False},
                "data_classes": profile}
    fname = os.path.join(profile_path, f"mdw_profiler_mysql_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    write_timestamp(f"write profile {fname}")
    export_json(json_out, fname)
    print()
    return


if '__main__' == __name__:
    main()
