import os
import json
import sqlite3
import datetime
import copy
import mdw_utilities as mdw

ML_DB = 'ml_db.db'
CWD = os.getcwd()

def test_and_try():
    conn = sqlite3.connect('ml_db.db')

    sql_statement = f"SELECT MAX(workflow_id) FROM PROFILER_INPUTS"

    cur = conn.cursor()
    cur.execute(sql_statement)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def load_profile(fname):
    mdw.write_timestamp(f"JSON load {fname}")
    json_in = mdw.get_json(fname)
    return json_in


def write_profile_to_profiler_inputs(json_profile):
    conn = sqlite3.connect(ML_DB)
    sql_statement = f"SELECT MAX(workflow_id) FROM PROFILER_INPUTS;"
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()

    row = rows[0]
    if row[0] is not None:
        workflow_id = row[0] + 1
    else:
        workflow_id = 0

    mdw.write_timestamp(f"write JSON profile to PROFILER_INPUTS with workflow id {workflow_id}")

    source_data_model = json_profile.get('dataset', f"profile_upload_{datetime.datetime.now().strftime('%Y%m%d')}")
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_profiler_str = json.dumps(json_profile)
    json_profiler_str = json_profiler_str.replace('"', '|')
    json_profiler_str = json_profiler_str.replace("'", "|")
    sql_statement = f"INSERT INTO PROFILER_INPUTS " \
                    f"('workflow_id', 'source_data_model_name', 'date_time_stamp', 'profiler_json_string') " \
                    f"VALUES ({workflow_id}, '{source_data_model}', '{time_stamp}', '{json_profiler_str}')"
    try:
        conn.execute(sql_statement)
        conn.commit()
    except Exception as e:
        mdw.write_timestamp(f"ERR: db insert {e}")

    rows = []
    sql_statement = f"SELECT * FROM PROFILER_INPUTS WHERE workflow_id = {workflow_id};"
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()

    mdw.write_timestamp(f"db commit for {len(rows)} rows")

    return workflow_id



def write_to_profiler_features(workflow_id):
    conn = sqlite3.connect(ML_DB)
    sql_statement = f"SELECT * FROM PROFILER_INPUTS WHERE workflow_id = {workflow_id};"
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()

    if len(rows) < 0:
        mdw.write_timestamp(f"no data in PROFILER_INPUTS for workflow ID {workflow_id}")
        return

    mdw.write_timestamp(f"extracting features for workflow id {workflow_id}")
    row = rows[0]
    input_id = row[0]
    wf_id = row[1]
    source_data_model_name = row[2]
    date_time_stamp = row[3]
    profiler_json_string = row[4]
    profiler_json_string = profiler_json_string.replace('|', '"')
    profiler_json = json.loads(profiler_json_string)

    data_class_id, data_element_id = 1, 0
    time_stamp = copy.deepcopy(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    data_classes = profiler_json.get('data classes', None)

    if not data_classes:
        return

    for dc_name, dc_data in data_classes.items():
        data_elements = dc_data.get('data elements', {})
        attribute_key = 'data class name'
        attribute_value = dc_name
        sql_statement = f"INSERT INTO PROFILER_FEATURES " \
                        f"('workflow_id', 'source_data_model_name', 'date_time_created', 'data_class_id', 'data_element_id', 'attribute_key', 'attribute_value') " \
                        f"VALUES ({workflow_id}, '{source_data_model_name}', '{time_stamp}', {data_class_id}, {data_element_id}, '{attribute_key}', '{attribute_value}');"
        try:
            conn.execute(sql_statement)
            conn.commit()
        except Exception as e:
            mdw.write_timestamp(f"ERR: db insert {e}")

        for data_element in data_elements:
            data_element_id += 1
            for de_key, de_value in data_element.items():
                attribute_value = f"{de_value}"
                if isinstance(attribute_value, str):
                    # attribute_value = attribute_value.replace('"', '|')
                    attribute_value = attribute_value.replace("'", '"')
                sql_statement = f"INSERT INTO PROFILER_FEATURES " \
                                f"('workflow_id', 'source_data_model_name', 'date_time_created', 'data_class_id', 'data_element_id', 'attribute_key', 'attribute_value') " \
                                f"VALUES ({workflow_id}, '{source_data_model_name}', '{time_stamp}', {data_class_id}, {data_element_id}, 'data element: {de_key}', '{attribute_value}');"
                try:
                    conn.execute(sql_statement)
                    conn.commit()
                except Exception as e:
                    mdw.write_timestamp(f"ERR: db insert {e}")
        data_class_id += 1
        data_element_id = 0

    # verify
    sql_statement = f"SELECT * FROM PROFILER_FEATURES WHERE workflow_id = {workflow_id};"
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()

    return


def main():
    fname = os.path.join(CWD, '00_data', 'text', 'panda_profiles', 'A&E Synthetic Data.json')
    json_profile = load_profile(fname)

    workflow_id = write_profile_to_profiler_inputs(json_profile)

    write_to_profiler_features(workflow_id)
    return


if '__main__'==__name__:
    main()

