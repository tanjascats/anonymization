# GLOBAL VARIABLES

# The k anonymization factor
K_FACTOR = 6

# Weight of the Generalization Information Loss
ALPHA = 1

# Target attribute
TARGET = 'education-num'

# Dataset file
DATASET_CSV = '../data/adult_grouped_sample.csv'

# Output directory
OUTPUT_DIR = '../output/samples/' + TARGET + '/'

# Directory containing hierarchies
GENH_DIR = 'data/gen_hierarchies/'

# Generalization hierarchies
GENH_FILE = {
    'workclass': 'WorkClassGH.json',
    'native-country': 'NativeCountryBinGH.json',
    'sex': 'SexGH.json',
    'race': 'RaceGH.json',
    'marital-status': 'MaritalStatusGH.json',
    'occupation': 'OccupationGH.json',
    'relationship': 'RelationshipGH.json',
    'income': 'IncomeGH.json'
}

# Weight vector for generalization categories
GEN_WEIGHT_VECTORS = {
    'equal': {
        'categorical': {
            'workclass': 1.0/12.0,
            'native-country': 1.0/12.0,
            'sex': 1.0/12.0,
            'race': 1.0/12.0,
            'marital-status': 1.0/12.0,
            'occupation': 1.0/12.0,
            'relationship': 1.0/12.0,
            'income': 1.0/12.0
        },
        'range': {
            'age': 1.0/12.0,
            'education-num': 1.0/12.0,
            'capital-gain': 1.0/12.0,
            'capital-loss': 1.0/12.0,
            'hours-per-week': 1.0/12.0
        }
    },
    'emph_race': {
        'categorical': {
            'workclass': 0.01,
            'native-country': 0.01,
            'sex': 0.01,
            'race': 0.89,
            'marital-status': 0.01,
            'occupation': 0.01,
            'relationship': 0.01,
            'income': 0.01
        },
        'range': {
            'age': 0.01,
            'education-num': 0.01,
            'capital-gain': 0.01,
            'capital-loss': 0.01,
            'hours-per-week': 0.01
        }
    },
    'emph_age': {
        'categorical': {
            'workclass': 0.01,
            'native-country': 0.01,
            'sex': 0.01,
            'race': 0.01,
            'marital-status': 0.01,
            'occupation': 0.01,
            'relationship': 0.01,
            'income': 0.01
        },
        'range': {
            'age': 0.89,
            'education-num': 0.01,
            'capital-gain': 0.01,
            'capital-loss': 0.01,
            'hours-per-week': 0.01
        }
    }
}

# Chosen weight vector
VECTOR = 'equal'

