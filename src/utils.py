import pandas as pd
import json


def read_input(csv_file):
    return pd.read_csv(csv_file, index_col=0)


def read_hierarchy(hierarchy_file):
    json_struct = read_from_json(hierarchy_file)
    entries = json_struct.get('entries')
    return entries


def read_from_json(json_file):
    file = open(json_file, 'r')
    return json.load(file)