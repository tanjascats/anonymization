## GLOBAL VARIABLES

# The k anonymization factor
K_FACTOR = 7

# Weight of the Generalization Information Loss
ALPHA = 1

# Weight of the Structural Information Loss
BETA = 0

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
            'relationship': 1.0/12.0
        },
        'range': {
            'age': 1.0/12.0,
            'education-num': 1.0/12.0,
            'capital-gain': 1.0/12.0,
            'capital-loss': 1.0/12.0,
            'hours-per-week': 1.0/12.0
        }
    },
    # necessary to change if I'm gonna use solutions with different weights
    'emph_race': {
        'categorical': {
            'workclass': 0.02,
            'native-country': 0.02,
            'sex': 0.02,
            'race': 0.9,
            'marital-status': 0.02,
        },
        'range': {
            'age': 0.02,
        }
    },
    'emph_age': {
        'categorical': {
            'workclass': 0.02,
            'native-country': 0.02,
            'sex': 0.02,
            'race': 0.02,
            'marital-status': 0.02,
        },
        'range': {
            'age': 0.9,
        }
    }
}

# Chosen weight vector
VECTOR = 'equal'
