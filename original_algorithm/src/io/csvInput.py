import pandas as pd

adult_file_name = '../../data/input_sanitized.csv'


def read_adults(file_name):
    adult_file = open(file_name, 'r')
    # read into pandas data frame
    adults_df = pd.read_csv(file_name, index_col=0)
    # convert to dict
    adults = adults_df.to_dict(orient='index')

    return adults


if __name__ == "__main__":
    print(read_adults(adult_file_name))
