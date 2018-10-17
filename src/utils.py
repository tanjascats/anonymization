import pandas as pd


def read_input(filepath):
    dataset = pd.read_csv(filepath, index_col=0)
    return pd.read_csv(filepath, index_col=0)