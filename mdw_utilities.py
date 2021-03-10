# Heiko Maerz MetadataWorks
# heiko@metadataworks.co.uk

# load packages
import copy
import datetime
import os
import pandas as pd
import requests
import json

# global variables
__version__ = '20201030_1751'


# timestamp
def write_timestamp(out_text=''):
    now = datetime.datetime.now().strftime("%Y/%m/%d %-H:%M:%S")
    print(f"{now} {out_text}")
    return


def get_json(json_uri):
    if isinstance(json_uri, dict):
        return json_uri
    elif os.path.isfile(json_uri):
        with open(json_uri, 'r') as json_file:
            return json.load(json_file)
    elif json_uri.startswith('http'):
        return requests.get(json_uri).json()
    else:
        raise Exception


def export_json(data, filename, indent=2):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=indent)


# write excel
def write_excel(fname, worksheets, idx=False):
    '''
    Write a number of worksheets to an Excel File
    :param fname: file path and file name
    :param worksheets: dictionary: {(worksheet name): (worksheet DataFrame), ...}
    :param idx: Boolean, save DataFrame indes to Excel, default False
    :return: None yet
    '''
    with pd.ExcelWriter(fname) as writer:
        for sheetname, df_worksheet in worksheets.items():
            df_worksheet.to_excel(writer, sheet_name=sheetname, index=idx)


def strip_string_to_alphanum(text_in):
    if not isinstance(text_in, str):
        return text_in

    text_out = ''
    for c in text_in:
        if c.isalnum():
            text_out = f"{text_out}{c}"
        elif c in (' ', '-', '_', '.', ','):
            text_out = f"{text_out}_"
    return text_out.strip()


def remove_none_from_dict(json_data):
    keys = copy.deepcopy(list(json_data.keys()))
    for js_key in keys:
        js_value = json_data.get(js_key, None)
        if isinstance(js_value, dict):
            remove_none_from_dict(js_value)
            if 0==len(list(js_value.keys())):
                json_data.pop(js_key, None)
        else:
            if not js_value:
                json_data.pop(js_key, None)
