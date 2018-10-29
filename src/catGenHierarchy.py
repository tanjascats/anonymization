import src.io.jsonInput as json


class CatGenHierarchy:

    def __init__(self, label, gen_file):
        self._label = ""
        self._entries = {}
        self._levels = 0
        self.read_from_json(gen_file)

    def read_from_json(self, json_file):
        json_struct = json.read_json(json_file)
        entries = json_struct.get('entries')
        self._entries = entries

        root_levels = 0
        for idx in entries:
            json_entry = entries[idx]

            level = int(json_entry.get('level'))
            self._levels = level if level > self._levels else self._levels
            if level == 0:
                root_levels += 1

        if root_levels != 1:
            raise Exception('JSON invalid. Level 0 must occur exactly once.')

    def get_entries(self):
        return self._entries

    def nr_levels(self):
        return self._levels

    def get_level_entry(self, key):
        return self._entries[key]['level']

    def get_generalization_of(self, key):
        return self._entries[key]['gen']

    def get_name_entry(self, key):
        return self._entries[key]['name']


if __name__ == '__main__':
    cgh = CatGenHierarchy('sex', '../data/gen_hierarchies/SexGH.json')
    print(cgh.get_entries())
    print(cgh.get_level_entry('Male'))