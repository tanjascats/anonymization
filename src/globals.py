import src.dataset as ds

DATASET_PATH = '../data/adult_sample.csv'
K = 3
# TODO
HIERARCHY_FILE_PATHS = {
    'marital-status': "../data/gen_hierarchies/MaritalStatusGH.json",
    'native-country': "../data/gen_hierarchies/NativeCountryBinGH.json",
    'occupation': "../data/gen_hierarchies/OccupationGH.json",
    'race': "../data/gen_hierarchies/RaceGH.json",
    'relationship': "../data/gen_hierarchies/RelationshipGH.json",
    'sex': "../data/gen_hierarchies/SexGH.json",
    'workclass': "../data/gen_hierarchies/WorkClassGH.json"
}