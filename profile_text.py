import datetime
import copy
import os
import platform
import pandas as pd
import pandas_profiling as pp
import requests
import statistics
import json

import innoUk_utilities as mdw


CWD = os.getcwd()
DATA_PATH = os.path.join(CWD, 'lcl_data', 'text', 'data')
PROFILE_PATH = os.path.join(CWD, 'lcl_data', 'text', 'panda_profiles')
SEPARATOR = ','
ROW_LIMIT = 10000
__version__ = '20210310.001'



# timestamp
def write_timestamp(out_text=''):
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f"{now} {out_text}")
    return


def write_header():
    write_timestamp(f"{__file__} version {__version__}")
    print(f"python=={platform.python_version()}")
    # print(f"numpy=={np.__version__}")
    print(f"pandas=={pd.__version__}")
    print(f"pandas_profiling=={pp.__version__}")
    print(f"requests=={requests.__version__}")
    print(f"{os.path.join(CWD, 'mdw_utilities.py')}=={mdw.__version__}")
    print()


def read_text_files(path, sep=SEPARATOR):
    write_timestamp(f"profile text files in '{path}'")
    profile = []
    all_keys = []

    files = os.listdir(path)

    for fname in files:
        if '.'==fname[0]:
            continue
        write_timestamp(f" - file '{fname}'")
        data_class = f"{os.path.splitext(fname)[0]}"
        if ROW_LIMIT > 0:
            df = pd.read_csv(os.path.join(path, fname), sep=sep, nrows=ROW_LIMIT)
        else:
            df = pd.read_csv(os.path.join(path, fname), sep=sep)
        write_timestamp(f"   start profile for {len(df)} rows")

        text_profile = pp.ProfileReport(df,
                                        title=f"Profile {fname}",
                                        config_file='pandas_profiler_config_mdw.yaml',
                                        dark_mode=True)
        write_timestamp(f"   convert to JSON")
        string_profile = text_profile.to_json()
        json_profile = json.loads(string_profile)
        text_profile = {data_class: {"data class": data_class, "file name": fname}}
        for key, value in json_profile.get('table', {}).items():
            if key in ['n', 'n_var', 'n_cells_missing', 'n_vars_with_missing', 'n_duplicates']: #, 'types']:
                text_profile[data_class][key] = value
        text_profile[data_class]["data elements"] = []
        for de_name, de_data in json_profile.get('variables', {}).items():
            de_profile = {'data element name': de_name}
            for de_key, de_value in de_data.items():
                all_keys.append(de_key)
                if de_key in ['count', 'type', 'n_distinct', 'is_unique', 'n_missing', 'count', 'mean', 'std',
                              'variance', 'min', 'max', 'range', '5%', '25%', '50%', '75%', '95%', 'n_category',
                              'value_counts_without_nan']:
                    if 'value_counts_without_nan'==de_key:
                        if len(de_value.keys()) < 33:
                            de_profile[de_key] = de_value
                    else:
                        de_profile[de_key] = de_value
            text_profile[data_class]["data elements"].append(de_profile)
        profile.append(text_profile)

    all_keys = list(set(all_keys))
    all_keys.sort()
    print()
    return profile


def write_pandas_profile(profile_path, profile):
    file_counter = 0
    for text_profile in profile:
        for class_name, class_profile in text_profile.items():
            json_out = {"MDW Profiler": "Flat Text Files",
                        "dataset": class_profile['file name'],
                        "version": __version__,
                        "profile date": datetime.datetime.now().strftime("%Y%m%dT%H%M%S"),
                        "row limit": ROW_LIMIT,
                        "data classes": {class_profile['data class']: class_profile}}
            fname = os.path.join(profile_path, f"{class_profile['data class']}.json")
            write_timestamp(f"write profile {fname}")
            mdw.export_json(json_out, fname)
            file_counter += 1
    write_timestamp(f"finished with {file_counter} files")
    print()
    return


def main():
    write_header()

    profile = read_text_files(os.path.join(CWD, DATA_PATH), sep=SEPARATOR)
    write_pandas_profile(os.path.join(CWD, PROFILE_PATH), profile)
    write_timestamp(f"done")
    return


if '__main__' == __name__:
    main()
