import datetime
import os
import platform
import pandas as pd
import pandas_profiling as pp
import requests
import json
import copy


CWD = os.getcwd()
DATA_PATH = os.path.join(CWD, 'lcl_data')
PROFILE_PATH = os.path.join(CWD, 'lcl_data', 'profiles')
FILES = ['A&E Synthetic Data.xlsx']
__version__ = '20210520'


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
    print()


def read_excel_files(path, files):
    write_timestamp(f"profile excel files in '{path}'")
    profile = []
    all_keys = []

    for fname in files:
        write_timestamp(f" - file '{fname}'")
        excel_file = read_excel_pd(os.path.join(path, fname), None)
        for data_class, df in excel_file.items():
            write_timestamp(f"   start profile for data class '{data_class}', {len(df)} rows")
            class_profile = pp.ProfileReport(df,
                                             title=f"Profile {data_class}",
                                             config_file='pandas_profiler_config_mdw.yaml',
                                             dark_mode=True)
            write_timestamp(f"   convert to JSON")
            string_profile = class_profile.to_json()
            json_profile = json.loads(string_profile)
            class_profile = {"data_class_name": data_class, "data_class_features": {"file name": fname}}
            for key, value in json_profile.get('table', {}).items():
                if key in ['n', 'n_var', 'n_cells_missing', 'n_vars_with_missing', 'n_duplicates']: #, 'types']:
                    class_profile["data_class_features"][key] = value
            class_profile["data_elements"] = []
            for de_name, de_data in json_profile.get('variables', {}).items():
                de_profile = {'data_element_name': de_name,
                              'data_type': de_data.get('type', ''),
                              'histogram': {},
                              'data_element_features': {}}
                if 0 < len(de_data.get('value_counts_without_nan', {})) <= 20:
                    de_histogram = ['value_counts_without_nan']
                    de_features = ['count', 'n_distinct', 'is_unique', 'n_missing', 'count', 'mean', 'std',
                                  'variance', 'min', 'max', 'range', '5%', '25%', '50%', '75%', '95%', 'n_category',
                                  'histogram']
                else:
                    de_histogram = ['histogram']
                    de_features = ['count', 'n_distinct', 'is_unique', 'n_missing', 'count', 'mean', 'std',
                                   'variance', 'min', 'max', 'range', '5%', '25%', '50%', '75%', '95%', 'n_category',
                                   'value_counts_without_nan']

                for de_key, de_value in de_data.items():
                    all_keys.append(de_key)
                    if de_key in de_features:
                        if 'value_counts_without_nan'==de_key:
                            if len(de_value.keys()) < 33:
                                de_profile['data_element_features'][de_key] = de_value
                        else:
                            de_profile['data_element_features'][de_key] = de_value
                    elif de_key in de_histogram:
                        if 'histogram' == de_key:
                            counts = de_value.get('counts', None)
                            bin_edges = de_value.get('bin_edges', None)
                            if counts and bin_edges:
                                zyzzyva = zip(bin_edges, counts)
                                zh = []
                                for z in zyzzyva:
                                    zh.append({'bin': z[0], 'count': z[1]})
                                de_profile[de_key] = zh
                        elif 'value_counts_without_nan' == de_key:
                            zh = []
                            for cat_key, cat_count in de_value.items():
                                zh.append({'key': cat_key, 'count': cat_count})
                            de_profile['histogram'] = zh

                class_profile["data_elements"].append(de_profile)
            profile.append(class_profile)

    all_keys = list(set(all_keys))
    all_keys.sort()
    print()
    return profile

def read_excel_pd(fname, fill_na = False):
    excel_reader = pd.ExcelFile(fname)
    work_sheets = excel_reader.sheet_names

    excel = {}

    for sheet in work_sheets:
        df_sheet = pd.DataFrame()
        df_sheet = pd.read_excel(excel_reader, sheet_name=sheet)
        if fill_na is not None:
            df_sheet.fillna('', inplace=True)
        excel[sheet] = copy.deepcopy(df_sheet)

    return excel


def write_pandas_profile(profile_path, profile):
    if len(profile) < 1:
        return
    json_out = {"profiler": "MDW excel files",
                "version": __version__,
                "profile_timestamp": datetime.datetime.now().strftime("%Y%m%dT%H%M%S"),
                "profiler_configuration": {"redaction": False},
                "data_classes": profile}
    fname = os.path.join(profile_path, f"mdw_profiler_excel_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    write_timestamp(f"write profile {fname}")
    export_json(json_out, fname)
    print()
    return

def export_json(data, filename, indent=2):
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=indent)
        return


def main():
    write_header()

    profile = read_excel_files(DATA_PATH, FILES)
    write_pandas_profile(os.path.join(CWD, PROFILE_PATH), profile)
    write_timestamp(f"done")
    return


if '__main__' == __name__:
    main()
