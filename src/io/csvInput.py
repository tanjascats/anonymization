import src.config as config

import pandas as pd
import numpy as np

adult_file_name = '../../data/input_sanitized.csv'

"""
Returns dataset dictionary, list of all attributes including target, 
list of names of numerical attributes and list of names of categorical attributes
"""


def read_dataset(file_name):
    adult_file = open(file_name, 'r')
    # read into pandas data frame
    dataset_df = pd.read_csv(file_name, index_col=0)
    # convert to dict
    adults = dataset_df.to_dict(orient='index')

    # get attributes
    columns = dataset_df.columns.tolist()
    # numerical attributes
    categorical = dataset_df.columns[dataset_df.dtypes == np.object].tolist()
    # categorical attributes
    numerical = dataset_df.columns[dataset_df.dtypes != np.object].tolist()
    if config.TARGET in categorical:
        categorical.remove(config.TARGET)
    elif config.TARGET in numerical:
        numerical.remove(config.TARGET)

    return adults, columns, numerical, categorical


if __name__ == "__main__":
    print(read_dataset(adult_file_name))
