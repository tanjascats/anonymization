import src.globals as glob
import src.utils as io
import numpy as np


class Dataset:

    def __init__(self):
        # the whole dataset
        self._dataset = io.read_input(glob.DATASET)
        # names of the attributes
        self._attributes = self._dataset.columns.tolist()[:-1]
        # numerical attributes
        self._categorical = self._dataset.columns[self._dataset.dtypes == np.object].tolist()[:-1]
        # categorical attributes
        self._numerical = self._dataset.columns[self._dataset.dtypes != np.object].tolist()[:-1]
        # ranges (min value, max value) for each numerical attribute
        self._ranges_numerical = {col: (min(self._dataset[col]), max(self._dataset[col])) for col in self._numerical}
        # number of hierarchy levels for each categorical attribute
        # TODO I need hierarchies for this
