import json


def read_json(json_file_path):
    json_file = open(json_file_path, 'r')
    return json.load(json_file)


if __name__ == '__main__':
    print(read_json('../../data/gen_hierarchies/SexGH.json'))