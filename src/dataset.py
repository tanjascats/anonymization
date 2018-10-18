import src.globals as glob
import src.utils as io
import numpy as np
from pprint import pprint


class Dataset:

    def __init__(self):
        # the whole dataset
        self._dataset = io.read_input(glob.DATASET_PATH)
        # names of the attributes
        self._attributes = self._dataset.columns.tolist()[:-1]
        # numerical attributes
        self._categorical = self._dataset.columns[self._dataset.dtypes == np.object].tolist()[:-1]
        # categorical attributes
        self._numerical = self._dataset.columns[self._dataset.dtypes != np.object].tolist()
        # ranges (min value, max value) for each numerical attribute
        self._ranges_numerical = {col: max(self._dataset[col]) - min(self._dataset[col]) for col in self._numerical}
        # number of hierarchy levels for each categorical attribute
        # TODO I need hierarchies for this
        for col in self._numerical:
            print(max(self._dataset[col]))
        print("Ranges found:")
        pprint(self._ranges_numerical)

    def get_size(self):
        return self._dataset.shape[0]

    def get_numerical(self):
        return self._numerical

    def get_categorical(self):
        return self._categorical

    def get_ranges(self):
        return self._ranges_numerical

    def get_attributes(self):
        return self._attributes

    def get_num_of_attributes(self):
        return len(self._attributes)

    def get_data(self):
        return self._dataset
