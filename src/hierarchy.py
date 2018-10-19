import src.utils as utils


class Hierarchy:
    def __init__(self, attribute, file_path):
        self._attribute = attribute
        self._file_path = file_path
        self._hierarchy = utils.read_hierarchy(self._file_path)

    def get_height(self):
        return max(self._hierarchy[key]['level'] for key in self._hierarchy.keys())

    def get_level(self, value):
        return self._hierarchy[value]['level']