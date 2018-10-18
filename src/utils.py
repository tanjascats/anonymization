import pandas as pd


def read_input(filepath):
    return pd.read_csv(filepath, index_col=0)
